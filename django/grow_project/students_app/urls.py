from django.urls import path
from . import views

urlpatterns = [
    path('', views.verify_with_dropdown, name='verify_dropdown'),
    path('<int:student_id>/avatar/', views.student_avatar, name='student_avatar'),
]
'''
urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('<int:student_id>/avatar/', views.student_avatar, name='student_avatar'),
]
'''