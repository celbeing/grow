# students_app/utils.py
import pandas as pd
import os
from django.conf import settings

CSV_PATH = os.path.join(settings.BASE_DIR, 'students.csv')

def load_students_from_csv():
    return pd.read_csv(CSV_PATH)

def validate_student_code_by_name(df, name: str, code: str):
    row = df[df["name"] == name]
    if row.empty:
        return None, "학생을 찾을 수 없습니다."
    student = row.iloc[0]
    if str(student["code"]).strip() != str(code).strip():
        return None, "코드가 일치하지 않습니다."
    return student.to_dict(), None

# 수학 아바타 이미지
def get_math_avatar_image(student_data):
    score_keys = [
        "math_problem_solving", "math_reasoning", "math_communication",
        "math_info_processing", "math_creative", "math_attitude"
    ]
    total = sum([int(student_data.get(key, 0)) for key in score_keys])

    if total <= 7:
        level = "lv1"
    elif total <= 14:
        level = "lv2"
    elif total <= 21:
        level = "lv3"
    else:
        level = "lvmax"

    return f"students_app/images/math_{level}.png"

# 사회 아바타 이미지
def get_social_avatar_image(student_data):
    score_keys = [
        "social_citizenship", "social_decision", "social_communication",
        "social_info", "social_critical"
    ]
    total = sum([int(student_data.get(key, 0)) for key in score_keys])

    if total <= 7:
        level = "lv1"
    elif total <= 14:
        level = "lv2"
    elif total <= 21:
        level = "lv3"
    else:
        level = "lvmax"

    return f"students_app/images/social_{level}.png"

# 과학 아바타 이미지
def get_science_avatar_image(student_data):
    score_keys = [
        "science_lifelong", "science_communication", "science_problem_solving",
        "science_inquiry", "science_logical"
    ]
    total = sum([int(student_data.get(key, 0)) for key in score_keys])

    if total <= 7:
        level = "lv1"
    elif total <= 14:
        level = "lv2"
    elif total <= 21:
        level = "lv3"
    else:
        level = "lvmax"

    return f"students_app/images/science_{level}.png"

