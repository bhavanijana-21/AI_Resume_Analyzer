def load_skills():

    with open("data/skills.txt", "r") as file:

        skills = file.read().splitlines()

    return skills


def extract_skills(text):

    skills_db = load_skills()

    found_skills = []

    for skill in skills_db:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    return found_skills