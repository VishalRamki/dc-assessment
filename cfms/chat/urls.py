from django.urls import path
from .views import ask_question_view

urlpatterns = [
    path('', ask_question_view, name='ask_question'),
]