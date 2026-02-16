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
        Extract skills using a predefined whitelist (keyword matching).
        This is much more accurate than generic noun chunking.
        """
        from .skills_data import SKILL_DB
        
        doc = self.nlp(text.lower())
        skills = set()
        
        # 1. Direct Token Match
        for token in doc:
            if token.text in SKILL_DB:
                skills.add(token.text)
                
        # 2. Phrase Matching (Simple N-gram lookahead for multi-word skills like "node.js" or "spring boot")
        # Converting text to list of words for simple sliding window
        words = [token.text for token in doc]
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            if bigram in SKILL_DB:
                skills.add(bigram)
                
        # 3. Handle special cases manually (e.g., C++, C# which might be split)
        if "c++" in text.lower(): skills.add("c++")
        if "c#" in text.lower(): skills.add("c#")
        if ".net" in text.lower(): skills.add(".net")

        return list(skills)
