from typing import List, Dict

class Scorer:
    @staticmethod
    def calculate_score(
        semantic_score: float,
        resume_skills: List[str],
        job_skills: List[str],
        experience_years: int = 0, # Placeholder
        required_years: int = 0    # Placeholder
    ) -> Dict:
        """
        Calculate final match score and detailed breakdown.
        Weights:
        - 50% Semantic (Vector Similarity)
        - 30% Skill Match (Jaccard/Overlap)
        - 20% Experience (Heuristic)
        """
        
        # 1. Skill Match Score
        # Normalize skills
        r_skills = set(s.lower() for s in resume_skills)
        j_skills = set(s.lower() for s in job_skills)
        
        if not j_skills:
            skill_score = 100.0 if r_skills else 0.0
            missing_skills = []
            present_skills = list(r_skills)
        else:
            intersection = r_skills.intersection(j_skills)
            # Use overlap coefficient or Jaccard? 
            # Ideally we want to know how many REQUIRED skills are present.
            # Assuming all JD skills are required for now.
            skill_score = (len(intersection) / len(j_skills)) * 100.0
            missing_skills = list(j_skills - r_skills)
            present_skills = list(intersection)

        # 2. Experience Score (Placeholder logic)
        # For now, we omit explicit experience parsing and assume neutral impact or 
        # rely on semantic score to capture experience level somewhat.
        # Adjusted Model: 60% Semantic + 40% Skills
        
        # Semantic score is usually 0.0-1.0 (Cosine), scale to 0-100
        # FAISS IP with normalized vectors returns Cosine Similarity (-1 to 1)
        sem_score_100 = max(0, semantic_score) * 100.0
        
        final_score = (0.6 * sem_score_100) + (0.4 * skill_score)
        
        return {
            "total_score": round(final_score, 1),
            "section_scores": {
                "semantic": round(sem_score_100, 1),
                "skills": round(skill_score, 1)
            },
            "missing_skills": missing_skills,
            "present_skills": present_skills
        }
    
    @staticmethod
    def generate_recommendations(missing_skills: List[str], score: float) -> List[str]:
        recommendations = []
        
        if score < 50:
            recommendations.append("The resume has low relevance to this job description. Consider tailoring your Summary and Experience sections.")
            
        if missing_skills:
            top_missing = missing_skills[:5]
            recommendations.append(f"Consider adding these missing skills: {', '.join(top_missing)}")
            recommendations.append("Add projects demonstrating these specific skills.")
            
        if score > 80:
            recommendations.append("Strong match! Focus on soft skills and culture fit in your interview prep.")
            
        return recommendations
