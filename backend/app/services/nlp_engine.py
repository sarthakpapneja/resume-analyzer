import spacy
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class NLPEngine:
    def __init__(self):
        print("Loading NLP models...")
        # Load spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model...")
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

        # Load Sentence Transformer for embeddings
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        print("NLP models loaded.")

    def get_embedding(self, text: str) -> np.ndarray:
        """Generate vector embedding for text."""
        message_embedding = self.encoder.encode(text)
        return message_embedding

    def extract_entities(self, text: str) -> dict:
        """Extract named entities (ORG, PERSON, GPE, etc.)."""
        doc = self.nlp(text)
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        return entities

    def compute_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return np.dot(vec1, vec2) / (norm1 * norm2)

    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills using a predefined list or simple NER heuristics.
        For production, this should use a dedicated Skill NER model or large lookup list.
        """
        # Placeholder: Extract capitalized words that might be skills, or use a small lookup
        # In a real app, load a skills.csv
        doc = self.nlp(text)
        skills = []
        # Heuristic: noun chunks or specific tokens
        # For now, we will rely on keyword matching from specific lists if available
        # or just return unique NOUNS/PROPNs as candidates
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
                skills.append(token.text)
        return list(set(skills))
