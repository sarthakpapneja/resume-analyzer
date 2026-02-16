from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import Optional
from app.models.schemas import AnalysisResponse
from app.services.parser import ResumeParser
from app.services.scorer import Scorer
from app.api.dependencies import get_nlp_engine
from app.services.nlp_engine import NLPEngine
from app.services.interview_generator import InterviewGenerator
from app.services.bullet_analyzer import BulletAnalyzer
from app.services.market_data import MarketDataService
from app.services.success_predictor import SuccessPredictor


router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    github_url: Optional[str] = Form(None),
    jd_file: Optional[UploadFile] = File(None),
    nlp_engine: NLPEngine = Depends(get_nlp_engine)
):
    try:
        # 1. Parse Resume
        content = await resume.read()
        filename = resume.filename.lower() if resume.filename else ""
        
        if filename.endswith(".pdf"):
            resume_text = ResumeParser.parse_pdf(content)
        elif filename.endswith(".docx"):
            resume_text = ResumeParser.parse_docx(content)
        else:
            resume_text = content.decode("utf-8", errors="ignore")
            
        if not resume_text:
             raise HTTPException(status_code=400, detail="Could not extract text from resume.")

        # 2. Parse Job Description (Text or File)
        jd_text = ""
        if jd_file:
            jd_content = await jd_file.read()
            jd_filename = jd_file.filename.lower() if jd_file.filename else ""
            
            if jd_filename.endswith(".pdf"):
                jd_text = ResumeParser.parse_pdf(jd_content)
            elif jd_filename.endswith(".docx"):
                jd_text = ResumeParser.parse_docx(jd_content)
            else:
                jd_text = jd_content.decode("utf-8", errors="ignore")
        elif job_description:
            jd_text = job_description
            
        if not jd_text:
            # If no JD provided, we can still analyze resume but JD-specific parts will be generic
            jd_text = "Generic Job Description" 

        # 3. Extract Entities & Skills (Resume)
        resume_entities = nlp_engine.extract_entities(resume_text)
        resume_skills = nlp_engine.extract_skills(resume_text)
        
        # 4. Process Job Description
        jd_skills = nlp_engine.extract_skills(jd_text)
        
        # 5. Generate Embeddings
        resume_vec = nlp_engine.get_embedding(resume_text)
        jd_vec = nlp_engine.get_embedding(jd_text)
        
        # 6. Calculate Score
        similarity_score = nlp_engine.compute_similarity(resume_vec, jd_vec)
        
        scoring_result = Scorer.calculate_score(
            semantic_score=similarity_score,
            resume_skills=resume_skills,
            job_skills=jd_skills
        )
        
        recommendations = Scorer.generate_recommendations(
            missing_skills=scoring_result["missing_skills"],
            score=scoring_result["total_score"]
        )

        # ATS Structural Checks (Basic)
        structure_analysis = {
            "file_size_kb": len(content) / 1024,
            "text_length": len(resume_text),
            "is_scanned_pdf": len(resume_text) < 200 and filename.endswith(".pdf"),
            "contact_info_present": "@" in resume_text # Simple check
        }
        
        if structure_analysis["is_scanned_pdf"]:
            recommendations.append("⚠️ CRITICAL: Your resume appears to be an image/scanned PDF. ATS cannot read it. Use a text-based PDF.")

        # 7. Calculate Trajectory
        trajectory = Scorer.calculate_trajectory(
            nlp_engine=nlp_engine,
            base_resume_text=resume_text,
            job_description=jd_text,
            missing_skills=scoring_result["missing_skills"],
            current_score=scoring_result["total_score"]
        )

        # 8. Generate Interview Questions
        interview_questions = InterviewGenerator.generate_questions(
            missing_skills=scoring_result["missing_skills"],
            job_skills=jd_skills
        )

        # 9. Analyze Bullets
        bullet_analysis = BulletAnalyzer.analyze_bullets(resume_text, nlp_engine=nlp_engine)

        # 10. Market Demand Analysis
        market_analysis = MarketDataService.get_market_data(resume_text, jd_text)
        
        # 11. Success Prediction
        success_prediction = SuccessPredictor.predict_success(
            resume_score=scoring_result["total_score"],
            missing_skills=scoring_result["missing_skills"],
            market_data=market_analysis
        )
        


        return AnalysisResponse(
            score=scoring_result["total_score"],
            missing_skills=scoring_result["missing_skills"],
            present_skills=scoring_result["present_skills"],
            recommendations=recommendations,
            trajectory=trajectory,
            interview_questions=interview_questions,
            bullet_analysis=bullet_analysis,
            market_analysis=market_analysis,
            success_prediction=success_prediction,
            github_analysis=None,
            structure_analysis=structure_analysis,
            resume_parsing_status="success"
        )

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
