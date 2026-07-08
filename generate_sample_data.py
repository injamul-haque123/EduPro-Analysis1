"""
Generates synthetic EduPro data (Users, Courses, Transactions) matching
the project's schema, so you can test the notebook and Streamlit app
before plugging in the real dataset.

Run once: python generate_sample_data.py
Produces: users.csv, courses.csv, transactions.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ---------------------------------------------------------------------
# USERS
# ---------------------------------------------------------------------
N_USERS = 1200

first_names = ["Aditi","Rohan","Priya","Karan","Sneha","Arjun","Meera","Vikram",
               "Ananya","Rahul","Ishaan","Divya","Kabir","Neha","Aarav","Riya",
               "Sara","Yusuf","Tara","Devika"]
last_names = ["Sharma","Verma","Gupta","Iyer","Khan","Reddy","Nair","Chatterjee",
              "Singh","Das","Menon","Rao","Kapoor","Joshi","Bose","Pillai"]

genders = np.random.choice(["Male", "Female", "Other"], size=N_USERS, p=[0.52, 0.45, 0.03])

# Age skewed toward 18-35 like a typical online learning platform
ages = np.clip(np.random.normal(loc=27, scale=9, size=N_USERS), 13, 70).astype(int)

users = pd.DataFrame({
    "UserID": [f"U{i:05d}" for i in range(1, N_USERS + 1)],
    "UserName": [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(N_USERS)],
    "Age": ages,
    "Gender": genders
})

# ---------------------------------------------------------------------
# COURSES
# ---------------------------------------------------------------------
categories = ["Data Science", "Programming", "Business", "Design",
              "Marketing", "Language Learning", "Personal Development", "Finance"]
course_types = ["Self-Paced", "Instructor-Led", "Cohort-Based"]
levels = ["Beginner", "Intermediate", "Advanced"]

course_name_templates = {
    "Data Science": ["Python for Data Analysis", "Machine Learning Foundations", "SQL for Analytics", "Data Visualization Masterclass"],
    "Programming": ["Java Programming Basics", "Full-Stack Web Development", "C++ Fundamentals", "Intro to Algorithms"],
    "Business": ["Business Strategy 101", "Entrepreneurship Essentials", "Operations Management", "Business Analytics"],
    "Design": ["UI/UX Design Principles", "Graphic Design Basics", "Figma for Beginners", "Design Thinking Workshop"],
    "Marketing": ["Digital Marketing Fundamentals", "SEO & Content Strategy", "Social Media Marketing", "Brand Management"],
    "Language Learning": ["Spanish for Beginners", "Business English", "French Conversation Practice", "Japanese Basics"],
    "Personal Development": ["Time Management Mastery", "Public Speaking Confidence", "Mindfulness & Productivity", "Career Planning"],
    "Finance": ["Personal Finance 101", "Investment Basics", "Financial Modeling", "Accounting Fundamentals"]
}

N_COURSES = 120
course_rows = []
cid = 1
for cat, names in course_name_templates.items():
    for _ in range(N_COURSES // len(course_name_templates)):
        course_rows.append({
            "CourseID": f"C{cid:04d}",
            "CourseName": np.random.choice(names),
            "CourseCategory": cat,
            "CourseType": np.random.choice(course_types, p=[0.5, 0.3, 0.2]),
            "CourseLevel": np.random.choice(levels, p=[0.5, 0.35, 0.15])
        })
        cid += 1

courses = pd.DataFrame(course_rows)

# ---------------------------------------------------------------------
# TRANSACTIONS (enrollments)
# ---------------------------------------------------------------------
N_TRANSACTIONS = 6000
start_date = datetime(2024, 1, 1)
end_date = datetime(2026, 6, 30)
date_range_days = (end_date - start_date).days

# Make enrollment count uneven across users (some very active, most casual)
user_weights = np.random.pareto(a=2.0, size=N_USERS) + 0.1
user_weights = user_weights / user_weights.sum()

# Beginners disproportionately pick Beginner-level courses; younger users skew
# toward Programming/Design, older users skew toward Business/Finance (for realism)
def pick_course_for_user(age):
    if age < 26:
        weights = courses["CourseCategory"].map({
            "Data Science": 1.3, "Programming": 1.5, "Design": 1.4, "Marketing": 1.0,
            "Business": 0.7, "Language Learning": 1.0, "Personal Development": 1.1, "Finance": 0.6
        }).values
    elif age < 40:
        weights = courses["CourseCategory"].map({
            "Data Science": 1.2, "Programming": 1.1, "Design": 1.0, "Marketing": 1.2,
            "Business": 1.3, "Language Learning": 0.8, "Personal Development": 1.0, "Finance": 1.1
        }).values
    else:
        weights = courses["CourseCategory"].map({
            "Data Science": 0.7, "Programming": 0.6, "Design": 0.7, "Marketing": 1.0,
            "Business": 1.4, "Language Learning": 0.9, "Personal Development": 1.2, "Finance": 1.4
        }).values
    weights = weights / weights.sum()
    return courses.iloc[np.random.choice(len(courses), p=weights)]["CourseID"]

user_idx = np.random.choice(N_USERS, size=N_TRANSACTIONS, p=user_weights)
tx_rows = []
for i, uidx in enumerate(user_idx):
    user_age = users.iloc[uidx]["Age"]
    course_id = pick_course_for_user(user_age)
    tx_date = start_date + timedelta(days=int(np.random.uniform(0, date_range_days)))
    tx_rows.append({
        "TransactionID": f"T{i+1:06d}",
        "UserID": users.iloc[uidx]["UserID"],
        "CourseID": course_id,
        "TransactionDate": tx_date.strftime("%Y-%m-%d")
    })

transactions = pd.DataFrame(tx_rows)

# ---------------------------------------------------------------------
# SAVE
# ---------------------------------------------------------------------
users.to_csv("users.csv", index=False)
courses.to_csv("courses.csv", index=False)
transactions.to_csv("transactions.csv", index=False)

print("Generated:")
print(f"  users.csv         -> {len(users)} rows")
print(f"  courses.csv       -> {len(courses)} rows")
print(f"  transactions.csv  -> {len(transactions)} rows")
