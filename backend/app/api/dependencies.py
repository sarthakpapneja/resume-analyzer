from app.services.nlp_engine import NLPEngine
from functools import lru_cache

@lru_cache()
def get_nlp_engine():
    """Singleton instance of NLP Engine to avoid reloading models."""
    return NLPEngine()
