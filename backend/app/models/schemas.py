from pydantic import BaseModel
from typing import List, Optional

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
    recommendations: List[str]
    resume_parsing_status: str
