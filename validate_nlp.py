import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.services.nlp_engine import NLPEngine
from app.services.skills_data import SKILL_DB

def test_extraction():
    print("⏳ Loading NLP Engine...")
    engine = NLPEngine()
    
    sample_text = """
    We are looking for a Software Engineer with experience in Python, React, and AWS.
    Candidates should have strong knowledge of Docker, Kubernetes, and CI/CD pipelines.
    Familiarity with machine learning (TensorFlow, PyTorch) is a plus.
    Must be a team player with good communication skills.
    Willingness to learn and flexible working hours.
    """
    
    print("\n📄 Sample Job Description:")
    print(sample_text.strip())
    
    print("\n🔍 Extracting Skills...")
    skills = engine.extract_skills(sample_text)
    
    print(f"\n✅ Extracted {len(skills)} Valid Skills:")
    print(", ".join(skills))
    
    # Validation
    garbage_words = ["willingness", "flexible", "player", "candidate"]
    found_garbage = [w for w in garbage_words if w in skills]
    
    if found_garbage:
        print(f"\n❌ FAILED: Found garbage words: {found_garbage}")
    else:
        print("\n✨ SUCCESS: No garbage words found!")

if __name__ == "__main__":
    test_extraction()
