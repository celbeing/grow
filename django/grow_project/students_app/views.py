from django.shortcuts import render,  redirect, get_object_or_404
from .models import Student

def verify_with_dropdown(request):
    error = None
    students = Student.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        input_code = request.POST.get('code')

        student = get_object_or_404(Student, id=student_id)

        if input_code == student.code:
            return redirect('student_avatar', student_id=student.id)
        else:
            error = "코드가 일치하지 않습니다."

    return render(request, 'students_app/verify_dropdown.html', {
        'students': students,
        'error': error
    })

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students_app/student_list.html', {'students': students})

def student_avatar(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students_app/student_avatar.html', {'student': student})
