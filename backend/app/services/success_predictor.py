from typing import Dict, List

class SuccessPredictor:
    @staticmethod
    def predict_success(
        resume_score: float,
        missing_skills: List[str],
        market_data: Dict
    ) -> Dict:
        """
        Predicts the probability of getting an interview based on various factors.
        """
        
        # Base probability is the resume score (normalized to 0-1)
        probability = resume_score / 100.0
        
        # Adjust based on Market Demand
        demand_level = market_data.get("demand_level", "Medium")
        if "Very High" in demand_level:
            probability += 0.15 # High demand means easier to get in
        elif "High" in demand_level:
            probability += 0.10
        elif "Low" in demand_level:
            probability -= 0.10
            
        # Penalize for critical missing skills
        # We assume the first 3 missing skills are "critical" for this heuristic
        critical_missing_count = min(len(missing_skills), 3)
        probability -= (critical_missing_count * 0.05)
        
        # Cap probability between 5% and 95%
        probability = max(0.05, min(0.95, probability))
        
        # Generate Tips
        tips = []
        if probability < 0.5:
             tips.append("Your resume score is low. Focus on adding more keywords.")
        if len(missing_skills) > 3:
             tips.append(f"Learn critical skills like {missing_skills[0]} and {missing_skills[1]}.")
        if "Low" in demand_level:
             tips.append("The market for this role is tough. Consider broadening your search.")
        else:
             tips.append("Market demand is on your side! Polish your resume to stand out.")
             
        return {
            "interview_probability": round(probability * 100, 1),
            "tips": tips
        }
