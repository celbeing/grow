from django.urls import path
from . import views

urlpatterns = [
    path('', views.avatar_view, name='avatar_view'),
    path('<int:student_id>/select_subject/', views.select_subject, name='select_subject'),
    path('<int:student_id>/<str:subject>/', views.show_avatar, name='show_avatar'),
]