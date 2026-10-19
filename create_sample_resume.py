"""
create_sample_resume.py
Run this script AFTER installing requirements to generate a sample_resume.pdf
for testing the Resume Analyser notebook.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

def create_sample_resume(output_path='sample_resume.pdf'):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()

    name_style = ParagraphStyle('Name', parent=styles['Title'],
                                fontSize=22, textColor=colors.HexColor('#1a73e8'))
    contact_style = ParagraphStyle('Contact', parent=styles['Normal'],
                                   fontSize=10, textColor=colors.grey)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'],
                                   fontSize=13, textColor=colors.HexColor('#1a73e8'),
                                   spaceBefore=10, spaceAfter=3)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14)
    bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'],
                                  fontSize=10, leading=13, leftIndent=12)

    story = []

    # Header
    story.append(Paragraph('Jane Smith', name_style))
    story.append(Paragraph(
        'jane.smith@email.com  •  +91 98765 43210  •  Bangalore, India  •  linkedin.com/in/janesmith  •  github.com/janesmith',
        contact_style))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#1a73e8')))
    story.append(Spacer(1, 0.2*cm))

    # Summary
    story.append(Paragraph('Professional Summary', heading_style))
    story.append(Paragraph(
        'Results-driven Software Engineer with 4 years of experience building scalable backend systems '
        'and APIs. Proficient in Python, Django, and REST API development. Passionate about cloud '
        'technologies and machine learning. Strong communicator with experience leading small development teams.',
        body_style))

    # Skills
    story.append(Paragraph('Technical Skills', heading_style))
    skills = [
        '<b>Languages:</b> Python, JavaScript, SQL, Bash',
        '<b>Frameworks:</b> Django, Flask, React.js, FastAPI',
        '<b>Cloud:</b> AWS (EC2, S3, Lambda), basic GCP',
        '<b>Tools:</b> Git, Docker, PostgreSQL, Redis, Jira, Postman',
        '<b>ML Libraries:</b> Pandas, NumPy, Scikit-learn, Matplotlib',
        '<b>Soft Skills:</b> Team Leadership, Agile, Communication, Problem Solving',
    ]
    for s in skills:
        story.append(Paragraph(f'• {s}', bullet_style))

    # Experience
    story.append(Paragraph('Work Experience', heading_style))
    story.append(Paragraph('<b>Software Engineer</b> — TechCorp Solutions, Bangalore', body_style))
    story.append(Paragraph('July 2022 – Present', contact_style))
    exp1 = [
        'Designed and developed REST APIs using Django and FastAPI serving 50K+ daily users.',
        'Reduced API response time by 40% through query optimization and Redis caching.',
        'Led a team of 3 junior developers, conducted code reviews and sprint planning.',
        'Deployed microservices on AWS EC2 and managed S3 storage buckets.',
        'Integrated Scikit-learn ML models into production pipelines for fraud detection.',
    ]
    for e in exp1:
        story.append(Paragraph(f'• {e}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('<b>Junior Python Developer</b> — StartupXYZ, Hyderabad', body_style))
    story.append(Paragraph('June 2020 – June 2022', contact_style))
    exp2 = [
        'Built data pipeline scripts in Python to automate ETL processes.',
        'Developed Flask-based internal dashboard for real-time reporting.',
        'Wrote unit tests and maintained 85%+ code coverage.',
    ]
    for e in exp2:
        story.append(Paragraph(f'• {e}', bullet_style))

    # Education
    story.append(Paragraph('Education', heading_style))
    story.append(Paragraph(
        '<b>B.Tech in Computer Science</b> — VIT University, Vellore (2020)  |  GPA: 8.4/10',
        body_style))

    # Projects
    story.append(Paragraph('Projects', heading_style))
    projects = [
        '<b>E-Commerce Analytics Dashboard</b>: Built a real-time dashboard using Django + Chart.js '
        'with PostgreSQL backend. Deployed on AWS EC2.',
        '<b>Sentiment Analysis API</b>: Created a REST API wrapping a fine-tuned BERT model for '
        'product review sentiment analysis. Used FastAPI + Docker.',
    ]
    for p in projects:
        story.append(Paragraph(f'• {p}', bullet_style))

    # Certifications
    story.append(Paragraph('Certifications', heading_style))
    certs = [
        'AWS Certified Developer – Associate (2023)',
        'Google Data Analytics Certificate (2022)',
    ]
    for c in certs:
        story.append(Paragraph(f'• {c}', bullet_style))

    doc.build(story)
    print(f'[OK] Sample resume created: {output_path}')


if __name__ == '__main__':
    create_sample_resume()
