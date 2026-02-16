from typing import List, Dict

# Static Question Bank
# In a production system, this would be a database or LLM call.
QUESTION_BANK = {
    "React": [
        "Explain the Virtual DOM and how it improves performance.",
        "What are Hooks? Compare useEffect vs useLayoutEffect.",
        "How do you optimize a React application for performance?",
        "Explain the concept of Higher-Order Components."
    ],
    "Node.js": [
        "Explain the Event Loop in Node.js.",
        "Difference between process.nextTick() and setImmediate().",
        "How does Node.js handle concurrency?",
        "Explain Streams and Buffers in Node.js."
    ],
    "Python": [
        "Explain the difference between list and tuple.",
        "What are decorators and how do you use them?",
        "Explain the Global Interpreter Lock (GIL).",
        "Difference between range() and xrange() in Python 2 vs 3."
    ],
    "SQL": [
        "Difference between INNER JOIN and LEFT JOIN.",
        "Explain ACID properties in databases.",
        "How do you optimize a slow SQL query?",
        "What is normalization? Explain 1NF, 2NF, 3NF."
    ],
    "Docker": [
        "Difference between an Image and a Container.",
        "Explain the purpose of Docker Compose.",
        "How do you optimize Docker image size?",
        "What is a multi-stage build?"
    ],
    "AWS": [
        "Difference between EC2 and Lambda.",
        "Explain S3 consistency models.",
        "What is an IAM Role vs IAM User?",
        "How do you secure an S3 bucket?"
    ],
    "System Design": [
        "How would you design a URL shortener like Bit.ly?",
        "Design a rate limiter.",
        "How do you handle database scaling (Sharding vs Replication)?",
        "Design a chat application like WhatsApp."
    ],
    "Behavioral": [
        "Tell me about a time you failed.",
        "How do you handle conflicts in a team?",
        "Describe a challenging project you worked on.",
        "Where do you see yourself in 5 years?"
    ]
}

class InterviewGenerator:
    @staticmethod
    def generate_questions(missing_skills: List[str], job_skills: List[str]) -> List[Dict[str, str]]:
        """
        Generate a tailored interview prep list.
        Prioritizes missing skills (Weaknesses) and key job skills (Strengths).
        Uses deterministic selection (first matching question per skill).
        """
        questions = []
        
        # 1. Target Weaknesses (Missing Skills)
        for skill in missing_skills:
            for key in QUESTION_BANK:
                if key.lower() in skill.lower() or skill.lower() in key.lower():
                    q_list = QUESTION_BANK[key]
                    questions.append({
                        "category": "Weakness / Missing Skill",
                        "skill": skill,
                        "question": q_list[0],  # Deterministic: always first question
                        "difficulty": "Hard"
                    })
                    break
        
        # 2. Verify Strengths (Job Skills that are matches)
        present_job_skills = set(job_skills) - set(missing_skills)
        
        for skill in sorted(present_job_skills):  # sorted for deterministic order
             for key in QUESTION_BANK:
                if key.lower() in skill.lower() or skill.lower() in key.lower():
                    q_list = QUESTION_BANK[key]
                    questions.append({
                        "category": "Strength / Verification",
                        "skill": skill,
                        "question": q_list[1] if len(q_list) > 1 else q_list[0],  # Second question for variety
                        "difficulty": "Medium"
                    })
                    break
        
        # 3. Always add Behavioral if we have few questions
        if len(questions) < 5:
            questions.append({
                "category": "Behavioral",
                 "skill": "Soft Skills",
                 "question": QUESTION_BANK["Behavioral"][0],  # Deterministic
                 "difficulty": "N/A"
            })
            
        # Limit to 7 questions
        return questions[:7]
