from fpdf import FPDF
import os

def create_sample_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="John Doe", ln=1, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Software Engineer | Python | React", ln=1, align='C')
    
    pdf.ln(10)
    
    # Skills
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Skills", ln=1, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Python, FastAPI, React, Next.js, Docker, Kubernetes, AWS, Machine Learning, NLP, spaCy, Pytorch")
    
    pdf.ln(5)
    
    # Experience
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Experience", ln=1, align='L')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Senior Developer at Tech Corp (2020 - Present)", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="- Built scalable microservices using FastAPI and Docker.\n- Led a team of 5 engineers to deploy ML models.\n- Optimized frontend performance using Next.js.")
    
    pdf.ln(5)
    
    # Education
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Education", ln=1, align='L')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="B.S. Computer Science, University of Technology", ln=1)

    os.makedirs("demo_data", exist_ok=True)
    pdf.output("demo_data/sample_resume.pdf")
    print("Created demo_data/sample_resume.pdf")

if __name__ == "__main__":
    try:
        create_sample_pdf()
    except Exception as e:
        print(f"Error: {e}")
        # Fallback if fpdf not installed (it's not in requirements.txt yet!)
