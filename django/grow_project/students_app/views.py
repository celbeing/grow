from django.shortcuts import render, get_object_or_404
from .models import Student

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students_app/student_list.html', {'students': students})

def student_avatar(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students_app/student_avatar.html', {'student': student})
