from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from app.models.schemas import AnalysisResponse
from app.services.parser import ResumeParser
from app.services.scorer import Scorer
from app.api.dependencies import get_nlp_engine
from app.services.nlp_engine import NLPEngine
import shutil
import os
import tempfile

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
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

        # 2. Extract Entities & Skills (Resume)
        resume_entities = nlp_engine.extract_entities(resume_text)
        resume_skills = nlp_engine.extract_skills(resume_text)
        
        # 3. Process Job Description
        jd_skills = nlp_engine.extract_skills(job_description)
        
        # 4. Generate Embeddings
        resume_vec = nlp_engine.get_embedding(resume_text)
        jd_vec = nlp_engine.get_embedding(job_description)
        
        # 5. Calculate Score
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
        
        return AnalysisResponse(
            score=scoring_result["total_score"],
            missing_skills=scoring_result["missing_skills"],
            recommendations=recommendations,
            resume_parsing_status="success"
        )

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
