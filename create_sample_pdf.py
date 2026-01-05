#!/usr/bin/env python3
"""
Create a sample PDF resume for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_sample_resume_pdf():
    """Create a sample resume PDF for testing"""
    
    # Create the PDF document
    doc = SimpleDocTemplate("sample_resume.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor='blue'
    )
    
    # Content
    story = []
    
    # Header
    story.append(Paragraph("John Doe", title_style))
    story.append(Paragraph("Senior Software Engineer", styles['Normal']))
    story.append(Paragraph("Email: john.doe@email.com | Phone: (555) 123-4567", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Professional Summary
    story.append(Paragraph("Professional Summary", heading_style))
    story.append(Paragraph(
        "Experienced software engineer with 5+ years in full-stack development, "
        "specializing in Python, JavaScript, and cloud technologies. Proven track "
        "record of delivering scalable web applications and leading cross-functional teams.",
        styles['Normal']
    ))
    story.append(Spacer(1, 15))
    
    # Technical Skills
    story.append(Paragraph("Technical Skills", heading_style))
    story.append(Paragraph("• Programming Languages: Python, JavaScript, TypeScript, Java", styles['Normal']))
    story.append(Paragraph("• Web Technologies: React, FastAPI, Node.js, HTML5, CSS3", styles['Normal']))
    story.append(Paragraph("• Databases: PostgreSQL, MongoDB, Redis", styles['Normal']))
    story.append(Paragraph("• Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD", styles['Normal']))
    story.append(Paragraph("• Tools: Git, Jira, VS Code, Postman", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Professional Experience
    story.append(Paragraph("Professional Experience", heading_style))
    
    story.append(Paragraph("Senior Software Engineer | Tech Corp | 2021 - Present", styles['Heading3']))
    story.append(Paragraph("• Developed and maintained 5+ web applications using Python and React", styles['Normal']))
    story.append(Paragraph("• Improved application performance by 40% through code optimization", styles['Normal']))
    story.append(Paragraph("• Led a team of 3 junior developers and conducted code reviews", styles['Normal']))
    story.append(Paragraph("• Implemented CI/CD pipelines reducing deployment time by 60%", styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Software Engineer | StartupXYZ | 2019 - 2021", styles['Heading3']))
    story.append(Paragraph("• Built RESTful APIs serving 10,000+ daily active users", styles['Normal']))
    story.append(Paragraph("• Collaborated with product team to define technical requirements", styles['Normal']))
    story.append(Paragraph("• Integrated third-party services and payment gateways", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Education
    story.append(Paragraph("Education", heading_style))
    story.append(Paragraph("Bachelor of Science in Computer Science", styles['Normal']))
    story.append(Paragraph("University of Technology | 2015 - 2019", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Certifications
    story.append(Paragraph("Certifications", heading_style))
    story.append(Paragraph("• AWS Certified Solutions Architect", styles['Normal']))
    story.append(Paragraph("• Google Cloud Professional Developer", styles['Normal']))
    story.append(Paragraph("• Certified Kubernetes Administrator (CKA)", styles['Normal']))
    
    # Build the PDF
    doc.build(story)
    print("✅ Sample resume PDF created: sample_resume.pdf")

if __name__ == "__main__":
    create_sample_resume_pdf()