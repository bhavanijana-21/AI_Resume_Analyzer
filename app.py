from flask import Flask, render_template, request
from flask import send_file
from reportlab.pdfgen import canvas
from matcher import match_resume_with_jd
from skills import extract_skills
from ats import calculate_ats
import pdfplumber

app = Flask(__name__)
latest_report = {}

def predict_role(jd_text):

    jd = jd_text.lower()

    if "python" in jd:
        return "Python Developer"

    elif "java" in jd:
        return "Java Developer"

    elif "react" in jd:
        return "Frontend Developer"

    elif "data analyst" in jd:
        return "Data Analyst"

    else:
        return "Software Developer"
def generate_questions(skills):

    questions = []

    skills = [s.lower() for s in skills]

    if "python" in skills:
        questions.extend([
            "What is OOP in Python?",
            "Difference between list and tuple?",
            "What is a decorator?"
        ])

    if "javascript" in skills:
        questions.extend([
            "What is closure in JavaScript?",
            "Difference between var, let and const?"
        ])

    if "git" in skills:
        questions.append(
            "What is the difference between merge and rebase?"
        )

    return questions[:5]

def extract_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():

    resume = request.files['resume']

    if not resume:
        return "Please upload a resume."

    if resume.filename == "":
        return "Please select a PDF file."

    if not resume.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed."


    text = extract_text(resume)
    jd_text = request.form['job_description']
    role = predict_role(jd_text)
    skills = extract_skills(text)
    questions = generate_questions(skills)

    match_score, matched, missing = \
        match_resume_with_jd(text, jd_text)
    ats_score, suggestions = \
        calculate_ats(text, skills,match_score,missing)
    total_required = len(matched) + len(missing)

    if total_required == 0:
        readiness = 0
    else:
        readiness = int((len(matched) / total_required) * 100)
    overall_score = round(
        (ats_score + match_score + readiness) / 3
    )
    if overall_score >= 80:
        strength = "Strong Candidate"
    elif overall_score >= 60:
        strength = "Average Candidate"
    else:
        strength = "Needs Improvement"
    tcs_score = min(overall_score + 15, 100)
    infosys_score = min(overall_score + 10, 100)
    wipro_score = min(overall_score + 8, 100)
    accenture_score = min(overall_score + 12, 100)
    capgemini_score = min(overall_score + 5, 100)    
    
    global latest_report

    latest_report.update({
        "ats_score": ats_score,
        "match_score": match_score,
        "readiness": readiness,
        "overall_score": overall_score,
        "role": role,
        "matched": matched,
        "missing": missing,
        "suggestions": suggestions,
        "questions": questions
   })
    roadmap = []
    for i, skill in enumerate(missing, start=1):
        roadmap.append(
            f"Week {i}: Learn {skill}"
        )

    return render_template(
        'result.html',
        resume_text=text,
        skills=skills,
        ats_score=ats_score,
        suggestions=suggestions,
        match_score=match_score,
        matched=matched,
        missing=missing,
        role=role,
        questions=questions,
        readiness=readiness,
        overall_score=overall_score,
        strength=strength,
        tcs_score=tcs_score,
        infosys_score=infosys_score,
        wipro_score=wipro_score,
        accenture_score=accenture_score,
        capgemini_score=capgemini_score,
        roadmap=roadmap
    )
@app.route("/download-report")
def download_report():
    print(latest_report)
    if not latest_report:
        return "Please analyze a resume first."

    pdf_file = "resume_report.pdf"

    c = canvas.Canvas(pdf_file)

    c.drawString(180, 800, "AI Resume Analyzer Report")

    c.drawString(
    100, 760,
    f"ATS Score: {latest_report['ats_score']}%"
    )

    c.drawString(
    100, 740,
    f"Job Match Score: {latest_report['match_score']}%"
    )

    c.drawString(
    100, 720,
     f"Readiness Score: {latest_report['readiness']}%"
    )

    c.drawString(
    100, 700,
    f"Overall Hiring Score: {latest_report['overall_score']}%"
    )

    c.drawString(
    100, 680,
    f"Predicted Role: {latest_report['role']}"
    )

    c.drawString(100, 640, "Matched Skills:")

    y = 620

    for skill in latest_report["matched"]:
        c.drawString(120, y, f"- {skill}")
        y -= 20

    c.drawString(100, y - 10, "Missing Skills:")

    y -= 35

    for skill in latest_report["missing"]:
        c.drawString(120, y, f"- {skill}")
        y -= 20

    c.drawString(100, y - 10, "Suggestions:")

    y -= 35

    for suggestion in latest_report["suggestions"]:
        c.drawString(120, y, f"- {suggestion}")
        y -= 20

    c.drawString(100, y - 10, "Interview Questions:")

    y -= 35

    for i, question in enumerate(
        latest_report["questions"], start=1
    ):
        c.drawString(
            120,
            y,
            f"{i}. {question}"
        )
        y -= 20
    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )    
if __name__ == '__main__':
    app.run(debug=True)