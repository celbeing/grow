from django.shortcuts import render, redirect
from .utils import load_students_from_csv, render_avatar_text, validate_student_code_by_name

def avatar_view(request):
    df = load_students_from_csv()
    names = df['name'].tolist()
    avatar_output = ""
    selected_name = ""
    error = ""

    if request.method == 'POST':
        selected_name = request.POST.get('student_name')
        code_input = request.POST.get('code')

        student_data, error = validate_student_code_by_name(df, selected_name, code_input)

        if not error:
            avatar_output = render_avatar_text("all", student_data)

    return render(request, 'students_app/avatar_form.html', {
        'student_names': names,
        'selected_name': selected_name,
        'avatar_output': avatar_output,
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
