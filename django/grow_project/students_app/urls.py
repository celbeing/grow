﻿from django.urls import path
from . import views

urlpatterns = [
    path('', views.avatar_view, name='avatar_view'),
    path('select_subject/', views.select_subject, name='select_subject'),
    path('avatar/<str:subject>/', views.show_avatar, name='show_avatar'),

    path('ajax/get_cities/', views.get_cities, name='get_cities'),
    path('ajax/get_schools/', views.get_schools, name='get_schools'),
    path('ajax/get_grades/', views.get_grades, name='get_grades'),
    path('ajax/get_names/', views.get_names, name='get_names'),
    path('ajax/update_score/', views.update_score, name='update_score'),
]