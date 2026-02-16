from pydantic import BaseModel
from typing import List, Optional, Optional

class ResumeContent(BaseModel):
    text: str
    skills: List[str] = []
    education: List[str] = []
    experience: List[str] = []

class JobDescription(BaseModel):
    text: str
    role_name: Optional[str] = None
    required_skills: List[str] = []

class AnalysisRequest(BaseModel):
    job_description: str

class AnalysisResponse(BaseModel):
    score: float
    missing_skills: List[str]
    present_skills: List[str]
    recommendations: List[str]
    trajectory: List[dict] = []
    interview_questions: List[dict] = []
    bullet_analysis: List[dict] = []
    market_analysis: dict = {}
    success_prediction: dict = {}
    github_analysis: Optional[dict] = None
    structure_analysis: dict = {}
    resume_parsing_status: str
