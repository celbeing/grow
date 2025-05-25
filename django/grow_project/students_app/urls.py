from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('<int:student_id>/avatar/', views.student_avatar, name='student_avatar'),
]
