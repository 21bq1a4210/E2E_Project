from django.urls import path
from . import views

app_name = 'ai_administration'

urlpatterns = [
    path('administration/', views.complaint_administration, name='ai_administration')
]

