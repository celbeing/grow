from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .utils import load_students_from_csv, render_avatar_text, get_math_avatar_image, get_social_avatar_image, get_science_avatar_image
import pandas as pd
import os

@csrf_exempt
def update_score(request):
    if request.method == "POST":
        student_id = int(request.POST.get("student_id"))
        key = request.POST.get("key")
        delta = int(request.POST.get("delta"))

        # CSV 경로 지정
        csv_path = os.path.join(settings.BASE_DIR, 'students.csv')
        df = pd.read_csv(csv_path)

        # 점수 수정
        idx = df.index[df["id"] == student_id].tolist()
        if not idx:
            return JsonResponse({"error": "학생을 찾을 수 없습니다."}, status=404)

        i = idx[0]
        old_score = int(df.at[i, key])
        new_score = max(0, min(50, old_score + delta))  # 0~50 제한
        df.at[i, key] = new_score
        df.to_csv(csv_path, index=False)

        return JsonResponse({"new_score": new_score})

# 학생 정보를 CSV 파일에서 불러오는 함수
# urls.py에서 이 함수들을 호출하여 AJAX 요청을 처리합니다.
def get_cities(request):
    region = request.GET.get("region")
    df = load_students_from_csv()
    cities = sorted(df[df["region"] == region]["city"].unique())
    return JsonResponse({"cities": cities})

def get_schools(request):
    region = request.GET.get("region")
    city = request.GET.get("city")
    df = load_students_from_csv()
    schools = sorted(df[(df["region"] == region) & (df["city"] == city)]["school"].unique())
    return JsonResponse({"schools": schools})

def get_grades(request):
    school = request.GET.get("school")
    df = load_students_from_csv()
    grade = sorted(df[df["school"] == school]["grade"].unique().tolist())
    return JsonResponse({"grade": grade})

def get_names(request):
    school = request.GET.get("school")
    grade = request.GET.get("grade")
    df = load_students_from_csv()
    names = df[(df["school"] == school) & (df["grade"] == int(grade))]["name"].tolist()
    return JsonResponse({"names": names})

def select_subject(request):
    # 코드 인증 성공 후 이 페이지로 redirect
    student_id = request.session.get('authenticated_student_id')
    
    # 세션 정보 일치하지 않는 경우
    if not student_id:
        return redirect('avatar_view')

    return render(request, 'students_app/select_subject.html', {
        'student_id': student_id
    })

def show_avatar(request, subject):
    student_id = request.session.get('authenticated_student_id')
    if not student_id:
        return redirect('avatar_view')
    
    df = load_students_from_csv()
    student_row = df[df["id"] == student_id]

    if student_row.empty:
        return HttpResponse("학생을 찾을 수 없습니다.")

    student_data = student_row.iloc[0].to_dict()

    if subject == "math":
        avatar_path = get_math_avatar_image(student_data)
        math_skills = {
            "math_problem_solving": "문제해결능력",
            "math_reasoning": "추론능력",
            "math_communication": "의사소통능력",
            "math_info_processing": "정보처리능력",
            "math_creative": "창의융합능력",
            "math_attitude": "태도 및 실천능력"
        }
        return render(request, "students_app/math.html", {
            "student": student_data,
            "avatar_path": avatar_path,
            "math_skills": math_skills
        })
    elif subject == "social":
        avatar_path = get_social_avatar_image(student_data)
        return render(request, "students_app/social.html", {
            "student": student_data,
            "avatar_path": avatar_path
        })
    elif subject == "science":
        avatar_path = get_science_avatar_image(student_data)
        return render(request, "students_app/science.html", {
            "student": student_data,
            "avatar_path": avatar_path
        })
    else:
        avatar_path = None  # 다른 과목 미구현 시 기본 처리
        return HttpResponse("잘못된 과목입니다.")

    

def avatar_view(request):
    df = load_students_from_csv()
    regions = sorted(df["region"].unique())
    error = ""
    
    if request.method == "POST":
        region = request.POST.get("region")
        city = request.POST.get("city")
        school = request.POST.get("school")
        grade = request.POST.get("grade")
        code = request.POST.get("code")

        try:
            filtered = df[
                (df["region"] == region) &
                (df["city"] == city) &
                (df["school"] == school) &
                (df["grade"] == int(grade)) &
                (df["code"] == code)
            ]

            if not filtered.empty:
                student_id = int(filtered.iloc[0]["id"])
                request.session['authenticated_student_id'] = student_id  # 세션에 저장
                return redirect("select_subject")
            else:
                error = "유효하지 않은 코드입니다."
        except:
           error = "모든 항목을 입력해 주세요."

    return render(request, "students_app/avatar_form.html", {
        "regions": regions,
        "error": error
    })

'''
def verify_with_dropdown(request):
    df = load_students_from_csv()
    names = df['name'].tolist()
    selected_name = ""
    result = ""
    error = ""

    if request.method == 'POST':
        selected_name = request.POST.get('student_name')
        code_input = request.POST.get('code')

        student_data, error = validate_student_code_by_name(df, selected_name, code_input)

        if not error:
            result = "인증 성공! (예: 아바타 페이지 이동)"

    return render(request, 'students_app/verify_dropdown.html', {
        'student_names': names,
        'selected_name': selected_name,
        'result': result,
        'error': error
    })
'''

def student_list(request):
    df = load_students_from_csv()
    return render(request, 'students_app/student_list.html', {'students': df.to_dict(orient='records')})
