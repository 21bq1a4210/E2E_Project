from django.urls import path, include
from . import views

# app_name = 'login'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path("feedback/", views.feedback, name='feedback'),
    path("", include("complaintbox.urls")),
    path("", include("chatbot.urls")),
    path("", include("lostAndFound.urls")),
    path("", include("FRS_attendance.urls")),
]
