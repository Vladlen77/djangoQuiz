from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='quiz-home'),
    path('timetable/', views.timetable, name='quiz-timetable'),
    path('rules/', views.rules, name='quiz-rules'),
    path('rating/', views.rating, name='quiz-rating'),
    path('game_rules/<str:game>/<str:time>/', views.game_rules, name='quiz-game_rules'),
    path('user_agreement/', views.user_agreement, name='quiz-user_agreement'),
]
