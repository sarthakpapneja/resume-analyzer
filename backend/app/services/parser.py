import io
import re
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document

class ResumeParser:
    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF bytes."""
        try:
            with io.BytesIO(file_bytes) as f:
                text = extract_pdf_text(f)
            return ResumeParser._clean_text(text)
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return ""

    @staticmethod
    def parse_docx(file_bytes: bytes) -> str:
        """Extract text from DOCX bytes."""
        try:
            with io.BytesIO(file_bytes) as f:
                doc = Document(f)
                text = "\\n".join([para.text for para in doc.paragraphs])
            return ResumeParser._clean_text(text)
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return ""

    @staticmethod
    def _clean_text(text: str) -> str:
        """Remove extra whitespace and artifacts."""
        # Replace multiple newlines with single newline
        text = re.sub(r'\\n+', '\\n', text)
        # Replace multiple spaces with single space
        text = re.sub(r'\\s+', ' ', text)
        return text.strip()

    @staticmethod
    def extract_sections(text: str) -> dict:
        """
        Heuristic-based section extraction.
        Returns a dict with 'education', 'experience', 'skills', 'projects' keys.
        """
        text_lower = text.lower()
        sections = {
            "education": "",
            "experience": "",
            "skills": "",
            "projects": ""
        }
        
        # Simple keyword markers
        markers = {
            "education": ["education", "academic background", "qualifications"],
            "experience": ["experience", "work history", "employment"],
            "skills": ["skills", "technical skills", "competencies", "technologies"],
            "projects": ["projects", "personal projects"]
        }
        
        # TODO: Implement more robust segmentation logic (e.g., regex finding headers)
        # For MVP, we will stick to full text processing or simple regex if needed.
        # Returning full text for now as sophisticated segmentation is complex without visual layout analysis.
        return sections
