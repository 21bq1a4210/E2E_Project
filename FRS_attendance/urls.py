from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('mark_attendance/<str:username>/', views.mark_attendance, name='mark_attendance'),
    path('face_recognition/', views.face_recognition, name='face_recognition'),  # Add this line
]
