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

# 아바타 텍스트 생성 함수
# 나중에 다 이미지 파일로 고쳐서 html+css+js로 렌더링할 예정
def render_avatar_text(subject: str, scores: dict):
    def level(score):
        if score <= 7: return "Lv.1"
        elif score <= 16: return "Lv.2"
        return "Lv.3"

    avatar_defs = {
        "math": ("제빵사", [
            ("모자", "math_problem_solving"),
            ("상의", "math_reasoning"),
            ("하의", "math_communication"),
            ("신발", "math_info_processing"),
            ("배경", "math_creative"),
            ("장갑", "math_attitude")
        ]),
        "social": ("시민", [
            ("모자", "social_citizenship"),
            ("상의", "social_decision"),
            ("하의", "social_communication"),
            ("신발", "social_info"),
            ("배경", "social_critical")
        ]),
        "science": ("탐정", [
            ("모자", "science_lifelong"),
            ("상의", "science_communication"),
            ("하의", "science_problem_solving"),
            ("신발", "science_inquiry"),
            ("배경", "science_logical")
        ])
    }

    output = []
    for subject_key in ["math", "social", "science"]:
        avatar_name, components = avatar_defs[subject_key]
        total = 0
        output.append(f"\n[{subject_key.upper()} 아바타 – {avatar_name}]")
        for part_name, stat in components:
            score = int(scores.get(stat, 0))
            total += score
            output.append(f"{part_name}: {part_name}_{level(score)} ({score})")

        # 아바타 레벨 계산
        if total <= 30:
            avatar_lv = "Lv.1"
        elif total <= 60:
            avatar_lv = "Lv.2"
        elif total <= 80:
            avatar_lv = "Lv.3"
        else:
            avatar_lv = "Lv.MAX"
        output.append(f"아바타 레벨: {avatar_lv} {avatar_name}")
    return "\n".join(output)
