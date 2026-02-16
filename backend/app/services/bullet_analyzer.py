import re
from typing import List, Dict

class BulletAnalyzer:
    @staticmethod
    def extract_bullets(text: str, nlp_engine=None) -> List[str]:
        """
        Extracts potential bullet points from text.
        Handles both well-formatted text (with newlines) and raw PDF text.
        """
        # Step 1: Split by newlines first
        raw_lines = text.split('\n')
        
        # Step 2: If PDF produced few lines, try splitting on bullet characters and sentence boundaries
        if len([l for l in raw_lines if l.strip()]) < 5:
            # Try splitting on bullet markers within long lines
            expanded = []
            for line in raw_lines:
                # Split on bullet markers (•, -, *, ◦) that appear mid-line
                parts = re.split(r'(?<=[.!?])\s+(?=[A-Z])|[•◦●]\s*|(?<=\s)[-*]\s+', line)
                expanded.extend(parts)
            raw_lines = expanded
        
        bullets = []
        
        # Headers and section titles to skip
        HEADER_WORDS = {
            'education', 'experience', 'skills', 'projects', 'certifications',
            'summary', 'objective', 'contact', 'references', 'achievements',
            'awards', 'publications', 'languages', 'interests', 'hobbies',
            'professional experience', 'work experience', 'technical skills',
            'core competencies', 'personal information', 'personal details'
        }
        
        for line in raw_lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip very short lines (likely headers, dates, names)
            if len(line) < 20:
                continue
            
            # Skip very long lines (likely paragraphs, not bullets)
            if len(line) > 300:
                continue

            # Remove leading bullet characters
            clean_line = re.sub(r'^[\u2022\u2023\u25E6\u2043\u2219\-\*\>\»]\s*', '', line).strip()
            
            if not clean_line or len(clean_line) < 15:
                continue
            
            # Skip all-uppercase headers (e.g., "EDUCATION", "WORK EXPERIENCE")
            if clean_line.isupper() and len(clean_line) < 50:
                continue
            
            # Skip known section headers
            if clean_line.lower().rstrip(':') in HEADER_WORDS:
                continue
                
            # Skip date-only lines (e.g., "Jan 2020 - Present")
            if re.match(r'^[A-Za-z]{3,9}\s+\d{4}\s*[-–—]\s*', clean_line):
                continue
            
            # Skip lines that look like contact info
            if re.match(r'^[\w.+-]+@[\w-]+\.[\w.]+$', clean_line):
                continue
            if re.match(r'^\+?\d[\d\s\-().]{7,}$', clean_line):
                continue
            
            # Skip lines that are mostly just a list of comma-separated skills
            comma_count = clean_line.count(',')
            word_count = len(clean_line.split())
            if comma_count > 3 and comma_count > word_count / 3:
                continue

            bullets.append(clean_line)
                     
        return bullets[:15]  # Analyze top 15 candidates

    @staticmethod
    def analyze_bullet(bullet: str, nlp_engine=None) -> Dict:
        score = 0
        suggestions = []
        
        # 0. NLP Analysis (optional enhancement)
        doc = nlp_engine.nlp(bullet) if nlp_engine else None
        
        # 1. Strong Action Verb Check
        has_strong_verb = False
        
        if doc:
            # Check if any verb in the sentence is a strong action verb
            for token in doc:
                if token.pos_ == "VERB" and token.lemma_.lower() in STRONG_ACTION_VERBS_SET:
                    has_strong_verb = True
                    break
        
        if not has_strong_verb:
            # Fallback: check first few words via regex
            words = re.findall(r'\w+', bullet.lower())
            for word in words[:5]:  # Check first 5 words
                if word in STRONG_ACTION_VERBS_SET:
                    has_strong_verb = True
                    break

        if has_strong_verb:
            score += 40
        else:
            suggestions.append("Start with a high-impact action verb (e.g., 'Spearheaded', 'Optimized' instead of 'Worked on').")

        # 2. Metrics Check (Quantifiable Impact)
        has_metrics = bool(re.search(r'\d+\s*%|\$\s*[\d,.]+|\d+\s*x\b|\d+\s*[kKmMbB]\b|\d+\s*(?:users?|customers?|clients?|projects?|teams?|people|members|employees|transactions|requests|queries|records|years?|months?|days?|hours?|minutes?)', bullet))
        if has_metrics:
            score += 40
        else:
            suggestions.append("Add metrics to prove value. (e.g., 'Reduced latency by 20%', 'Managed $50k budget', 'Served 10k users').")

        # 3. Length & Structure Check
        word_count = len(bullet.split())
        if 8 <= word_count <= 35:
            score += 20
        elif word_count < 8:
             suggestions.append("Too short. Add context: What did you do, How did you do it, and What was the result?")
        else:
             suggestions.append("Too long/run-on. Split into concise points.")
             
        # 4. Vagueness Penalty (no metrics AND no strong verb = vague)
        if not has_metrics and not has_strong_verb:
             score = max(0, score - 10)
             suggestions.append("Vague statement. Use the 'XYZ Method': 'Accomplished [X] as measured by [Y], by doing [Z]'.")

        return {
            "text": bullet,
            "score": score,
            "suggestions": suggestions
        }

    @staticmethod
    def analyze_bullets(text: str, nlp_engine=None) -> List[Dict]:
        raw_bullets = BulletAnalyzer.extract_bullets(text, nlp_engine)
        analysis = []
        
        for b in raw_bullets:
            result = BulletAnalyzer.analyze_bullet(b, nlp_engine)
            # Include all bullets that need any improvement (score < 100)
            if result['score'] < 100:
                analysis.append(result)
        
        # Sort by lowest score first
        analysis.sort(key=lambda x: x['score'])
        return analysis[:10]  # Return top 10


# Strong action verbs set
STRONG_ACTION_VERBS_SET = {
    "achieved", "accelerated", "accomplished", "added", "advanced", "analyzed",
    "architected", "attained", "augmented", "awarded", "bootstrapped",
    "built", "calculated", "capitalized", "championed", "collaborated", "composed",
    "computed", "conceived", "consolidated", "constructed", "converted", "coordinated",
    "created", "debugged", "decreased", "defined", "delivered", "deployed",
    "designed", "developed", "devised", "diagnosed", "directed", "distributed",
    "documented", "doubled", "drove", "earned", "eliminated", "empowered",
    "engineered", "enhanced", "established", "estimated", "evaluated", "exceeded",
    "expanded", "expedited", "facilitated", "forecasted", "formulated", "founded",
    "generated", "guided", "hired", "identified", "implemented", "improved",
    "increased", "initiated", "innovated", "installed", "integrated", "introduced",
    "invented", "investigated", "launched", "led", "leveraged", "managed",
    "maximized", "mentored", "migrated", "minimized", "modeled", "modified",
    "negotiated", "optimized", "orchestrated", "organized", "originated", "outperformed",
    "overcame", "overhauled", "pioneered", "planned", "predicted", "produced",
    "programmed", "promoted", "proposed", "provided", "published", "qualified",
    "quantified", "reached", "rebuilt", "reduced", "refactored", "refined",
    "reorganized", "resolved", "restructured", "revamped", "reviewed", "revitalized",
    "saved", "scaled", "secured", "selected", "separated", "simplified",
    "sold", "solved", "spearheaded", "standardized", "started", "streamlined",
    "strengthened", "structured", "succeeded", "supervised", "supported",
    "surpassed", "synthesized", "targeted", "taught", "tested", "trained",
    "transformed", "translated", "tripled", "updated", "upgraded", "utilized",
    "validated", "verified", "visualized", "won", "wrote"
}
