from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='quiz-home'),
    path('timetable/', views.timetable, name='quiz-timetable'),
    path('rules/', views.rules, name='quiz-rules'),
]