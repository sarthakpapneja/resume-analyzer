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
        
        # Adjusted Model: 60% Semantic + 40% Skills
        
        # Semantic score is usually 0.0-1.0 (Cosine), scale to 0-100
        # FAISS IP with normalized vectors returns Cosine Similarity (-1 to 1)
        sem_score_100 = max(0.0, float(semantic_score)) * 100.0
        
        final_score = (0.6 * sem_score_100) + (0.4 * skill_score)
        
        return {
            "total_score": int(round(final_score)),
            "section_scores": {
                "semantic": int(round(sem_score_100)),
                "skills": int(round(skill_score))
            },
            "missing_skills": missing_skills,
            "present_skills": present_skills
        }
    
    @staticmethod
    def generate_recommendations(missing_skills: List[str], score: float) -> List[str]:
        recommendations = []
        
        # 1. Score-based generic advice
        if score < 50:
            recommendations.append("Match Score Low: Your resume covers less than 50% of the key requirements. Tailor your 'Summary' and 'Experience' sections to mirror the job language.")
        elif score < 75:
            recommendations.append("Good Foundation: You have a solid base. Bridge the gap by highlighting specific projects that use the missing tools.")
        else:
            recommendations.append("Top Candidate: High match score! Focus your interview prep on behavioral questions and system design.")

        if not missing_skills:
            return recommendations

        # 2. Category-based specific advice
        try:
            from .skills_data import SKILL_CATEGORIES
            
            missing_set = set(missing_skills)
            categories_missing = {}

            for category, skills in SKILL_CATEGORIES.items():
                overlap = missing_set.intersection(skills)
                if overlap:
                    categories_missing[category] = list(overlap)

            # Generate advice based on top missing categories
            if "DevOps & Cloud" in categories_missing:
                tools = ", ".join(categories_missing["DevOps & Cloud"][:3])
                recommendations.append(f"☁️ Cloud Gap: The role requires cloud/DevOps skills ({tools}). Consider a mini-project deploying an app to AWS/GCP.")
                
            if "AI/ML" in categories_missing:
                 tools = ", ".join(categories_missing["AI/ML"][:3])
                 recommendations.append(f"🤖 AI/ML Gap: Missing key data stack skills ({tools}). Highlight any data processing or modeling experience.")
            
            if "Frontend" in categories_missing:
                tools = ", ".join(categories_missing["Frontend"][:3])
                recommendations.append(f"🎨 Frontend Gap: Key frameworks missing ({tools}). ensure they are listed in your 'Skills' section if you know them.")
                
            if "Database" in categories_missing:
                tools = ", ".join(categories_missing["Database"][:3])
                recommendations.append(f"🗄️ Database Gap: Mention your experience with specific DBs ({tools}) to show backend depth.")

            # 3. Soft Skills check
            if "Soft Skills" in categories_missing:
                 recommendations.append("Soft Skills: Don't forget to weave leadership and communication keywords into your bullet points.")

        except ImportError:
            # Fallback if skills_data not found in context (e.g. tests)
            pass

        return recommendations

    @staticmethod
    def calculate_trajectory(
        nlp_engine,
        base_resume_text: str,
        job_description: str,
        missing_skills: List[str],
        current_score: float
    ) -> List[Dict]:
        """
        Simulate how learning specific missing skills impacts the score.
        Returns a list of improvements: { "skill": "React", "new_score": 75, "boost": 15 }
        """
        trajectory = []
        
        # Limit simulation to top 5 impactful skills to save compute
        skills_to_sim = missing_skills[:5]
        
        # Pre-compute JD embedding once
        jd_vec = nlp_engine.get_embedding(job_description)
        jd_skills = nlp_engine.extract_skills(job_description) # Re-extract to be safe/consistent
        
        for skill in skills_to_sim:
            # 1. Augment Text
            # We append the skill to the text to simulate "learning" it
            augmented_text = base_resume_text + f" I have advanced experience with {skill}."
            
            # 2. Re-calculate Embeddings
            aug_vec = nlp_engine.get_embedding(augmented_text)
            
            # 3. Re-calculate Similarity
            new_sem_score = nlp_engine.compute_similarity(aug_vec, jd_vec)
            
            # 4. Re-calculate Skill Score
            # We assume we now HAVE this skill
            temp_resume_skills = nlp_engine.extract_skills(base_resume_text) + [skill]
            
            # Reuse core scoring logic (lighter version)
            r_skills = set(s.lower() for s in temp_resume_skills)
            j_skills = set(s.lower() for s in jd_skills)
            
            if not j_skills:
                new_skill_score = 100.0 if r_skills else 0.0
            else:
                intersection = r_skills.intersection(j_skills)
                new_skill_score = (len(intersection) / len(j_skills)) * 100.0
            
            sem_score_100 = max(0.0, float(new_sem_score)) * 100.0
            new_final_score = (0.6 * sem_score_100) + (0.4 * new_skill_score)
            new_final_score = int(round(new_final_score))
            
            boost = new_final_score - int(round(current_score))
            
            if boost > 0:
                trajectory.append({
                    "skill": skill,
                    "new_score": new_final_score,
                    "boost": boost
                })
                
        # Sort by impact
        trajectory.sort(key=lambda x: x["boost"], reverse=True)
        return trajectory
