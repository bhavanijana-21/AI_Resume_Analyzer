def match_resume_with_jd(resume_text, jd_text):

    skills_db = [
        "Python",
        "Java",
        "C",
        "C++",
        "HTML",
        "CSS",
        "JavaScript",
        "TypeScript",
        "React",
        "Angular",
        "Vue",
        "Node.js",
        "Express.js",
        "Flask",
        "Django",
        "FastAPI",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Git",
        "GitHub",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure",
        "Linux",
        "REST API",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy",
        "Data Analysis",
        "Power BI",
        "Tableau"
    ]

    matched = []
    missing = []

    for skill in skills_db:

        if skill.lower() in jd_text.lower():

            if skill.lower() in resume_text.lower():
                matched.append(skill)
            else:
                missing.append(skill)

    total = len(matched) + len(missing)

    if total == 0:
        score = 0
    else:
        score = int((len(matched) / total) * 100)

    return score, matched, missing