from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .utils import load_students_from_csv, render_avatar_text, validate_student_code_by_name, get_science_avatar_image

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

def select_subject(request, student_id):
    # 코드 인증 성공 후 이 페이지로 redirect
    return render(request, 'students_app/select_subject.html',{
        'student_id': student_id
    })

def show_avatar(request, student_id, subject):
    # 선택된 과목을 기반으로 아바타 출력
    # 이 부분은 나중에 이미지로 대체할 예정
    df = load_students_from_csv()
    student_row = df[df["id"] == student_id]

    if student_row.empty:
        return HttpResponse("학생을 찾을 수 없습니다.")

    student_data = student_row.iloc[0].to_dict()

    if subject == "science":
        avatar_path = get_science_avatar_image(student_data)
    else:
        avatar_path = None  # 다른 과목 미구현 시 기본 처리

    return render(request, "students_app/science.html", {
        "student": student_data,
        "avatar_path": avatar_path
    })


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
                return redirect("select_subject", student_id=student_id)
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
