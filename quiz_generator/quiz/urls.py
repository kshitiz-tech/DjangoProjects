from django.urls import path
from . import views

urlpatterns = [
    path("", views.index,name = 'index'),
    path("quiz_generator", views.quiz_generator,name="generate_quiz")
]