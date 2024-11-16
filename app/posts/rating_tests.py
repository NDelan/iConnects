import os
from rating import rate_resume_for_keywords
from post_matching_algorithm import match_posts_to_resume
from pdf_to_text import to_text

resume_text = to_text("/Users/adjei.net/Desktop/iConnects-Del/app/static/images/Eric_Adjei_Resume.pdf")

keywords = ["Python", "machine learning", "JavaScript", "data analysis", "cloud computing"]

print("Keyword Ratings:")
ratings = rate_resume_for_keywords(resume_text, keywords)
for keyword, rating in ratings.items():
    print(f"{keyword}: {rating}")

posts = {
    "Marketing Specialist": {"SEO": 18, "content creation": 17, "social media": 15, "analytics": 12},
    "Mechanical Engineer": {"CAD": 20, "mechanics": 18, "mathematics": 15, "project management": 10},
    "Financial Analyst": {"Excel": 20, "data analysis": 18, "forecasting": 15, "finance": 20},
    "Registered Nurse": {"patient care": 20, "medication administration": 18, "medical knowledge": 15, "communication": 12},
    "High School Teacher": {"lesson planning": 17, "subject knowledge": 20, "classroom management": 15, "communication": 18},
    "Event Coordinator": {"event planning": 20, "communication": 18, "budgeting": 15, "logistics": 17},
    "Graphic Designer": {"Photoshop": 20, "creativity": 18, "layout design": 15, "branding": 10},
    "Civil Engineer": {"AutoCAD": 20, "construction": 15, "project management": 18, "mathematics": 12},
    "Sales Representative": {"sales strategies": 20, "communication": 18, "CRM software": 15, "negotiation": 17},
    "Human Resources Manager": {"recruitment": 20, "employee relations": 18, "HR software": 15, "communication": 12},
    "Chef": {"menu planning": 18, "culinary skills": 20, "inventory management": 15, "creativity": 17},
    "Electrician": {"wiring": 20, "blueprint reading": 15, "safety protocols": 18, "problem-solving": 12},
    "Customer Service Representative": {"communication": 20, "problem-solving": 18, "CRM software": 15, "patience": 17},
    "Pharmacist": {"pharmaceutical knowledge": 20, "inventory management": 15, "patient interaction": 18, "organization": 12},
    "Digital Marketing Manager": {"SEO": 20, "PPC advertising": 18, "content marketing": 15, "analytics": 12}
}

print("\nTop Post Matches:")
matched_posts = match_posts_to_resume(posts, ratings, number_of_post_matches=3)
for score, title in matched_posts:
    print(f"{title} with difference score: {score}")
