def calculate_ats(text, skills, match_score, missing):

    score = 0
    suggestions = []

    text = text.lower()

    if "github" not in text:
        suggestions.append("Add GitHub profile")

    if "linkedin" not in text:
        suggestions.append("Add LinkedIn profile")

    if len(skills) < 5:
        suggestions.append("Add more technical skills")

    score += min(len(skills) * 3, 30)

    if "education" in text:
        score += 15

    if "project" in text:
        score += 15

    if "internship" in text:
        score += 15

    if "github" in text:
        score += 10

    if "linkedin" in text:
        score += 10

    if "certification" in text:
        score += 10

    score += int(match_score * 0.15)

    missing_lower = [skill.lower() for skill in missing]

    if "sql" in missing_lower:
        suggestions.append(
            "Improve SQL and database concepts."
        )

    if "flask" in missing_lower:
        suggestions.append(
            "Learn Flask for backend web development."
        )

    if "docker" in missing_lower:
        suggestions.append(
            "Learn Docker for deployment and containerization."
        )

    if "aws" in missing_lower:
        suggestions.append(
            "Learn AWS cloud fundamentals."
        )

    if "rest api" in missing_lower:
        suggestions.append(
            "Practice building REST APIs."
        )

    if "linux" in missing_lower:
        suggestions.append(
            "Improve Linux command-line skills."
        )


    return min(score, 100), suggestions