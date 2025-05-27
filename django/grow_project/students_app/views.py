from django.shortcuts import render, redirect
from .utils import load_students_from_csv, render_avatar_text, validate_student_code_by_name

def select_subject(request, student_id):
    # 코드 인증 성공 후 이 페이지로 redirect
    return render(request, 'students_app/select_subject.html',{
        'student_id': student_id
    })

def show_avatar(request, subject):
    # 선택된 과목을 기반으로 아바타 출력
    # 이 부분은 나중에 이미지로 대체할 예정
    return render(request, 'students_app/avatar.html', {
        'subject': subject
    })


def avatar_view(request):
    df = load_students_from_csv()
    names = df['name'].tolist()
    selected_name = ""
    error = ""

    if request.method == 'POST':
        selected_name = request.POST.get('student_name')
        code_input = request.POST.get('code')

        student_data, error = validate_student_code_by_name(df, selected_name, code_input)

        if not error:
            student_id = student_data['id']
            return redirect('select_subject', student_id=student_id)

    return render(request, 'students_app/avatar_form.html', {
        'student_names': names,
        'selected_name': selected_name,
        'error': error
    })


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


def student_list(request):
    df = load_students_from_csv()
    return render(request, 'students_app/student_list.html', {'students': df.to_dict(orient='records')})
