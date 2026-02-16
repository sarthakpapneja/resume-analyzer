import random
from typing import Dict, List

# Static database of market data for common tech roles
MARKET_DATA = {
    "software engineer": {
        "salary_range": "$90k - $160k",
        "demand_level": "High",
        "demand_growth": "+12%",
        "top_skills": ["Python", "Java", "Docker", "AWS", "React"],
        "avg_tenure": "2.1 years"
    },
    "frontend developer": {
        "salary_range": "$80k - $140k",
        "demand_level": "Medium-High",
        "demand_growth": "+8%",
        "top_skills": ["React", "TypeScript", "Tailwind", "Next.js", "Figma"],
        "avg_tenure": "1.8 years"
    },
    "backend developer": {
        "salary_range": "$95k - $165k",
        "demand_level": "High",
        "demand_growth": "+15%",
        "top_skills": ["Python", "Go", "PostgreSQL", "Redis", "Kubernetes"],
        "avg_tenure": "2.3 years"
    },
    "data scientist": {
        "salary_range": "$110k - $190k",
        "demand_level": "Very High",
        "demand_growth": "+22%",
        "top_skills": ["Python", "PyTorch", "SQL", "Machine Learning", "AWS"],
        "avg_tenure": "2.5 years"
    },
    "product manager": {
        "salary_range": "$100k - $180k",
        "demand_level": "Medium",
        "demand_growth": "+5%",
        "top_skills": ["Agile", "Jira", "Strategy", "User Research", "SQL"],
        "avg_tenure": "2.0 years"
    },
    "devops engineer": {
        "salary_range": "$115k - $185k",
        "demand_level": "High",
        "demand_growth": "+18%",
        "top_skills": ["AWS", "Terraform", "Kubernetes", "CI/CD", "Python"],
        "avg_tenure": "2.2 years"
    },
    "full stack developer": {
        "salary_range": "$100k - $170k",
        "demand_level": "High",
        "demand_growth": "+14%",
        "top_skills": ["React", "Node.js", "TypeScript", "SQL", "AWS"],
        "avg_tenure": "2.0 years"
    }
}

class MarketDataService:
    @staticmethod
    def get_market_data(resume_text: str, job_description: str = "") -> Dict:
        """
        Determines the role from resume/JD and returns market data.
        """
        text_to_search = (job_description + " " + resume_text).lower()
        
        # Simple keyword matching to find the role
        detected_role = "software engineer" # Default
        
        # Check specific roles first (longer matches first)
        if "data scientist" in text_to_search:
            detected_role = "data scientist"
        elif "product manager" in text_to_search:
            detected_role = "product manager"
        elif "devops" in text_to_search or "sre" in text_to_search:
            detected_role = "devops engineer"
        elif "frontend" in text_to_search or "front-end" in text_to_search:
            detected_role = "frontend developer"
        elif "backend" in text_to_search or "back-end" in text_to_search:
            detected_role = "backend developer"
        elif "full stack" in text_to_search or "fullstack" in text_to_search:
            detected_role = "full stack developer"

        data = MARKET_DATA.get(detected_role, MARKET_DATA["software engineer"])
        
        return {
            "role": detected_role.title(),
            **data
        }
