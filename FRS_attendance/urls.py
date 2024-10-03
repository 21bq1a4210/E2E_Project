from django.urls import path, include
from . import views

urlpatterns = [
    path('face_recognition/', views.face_recognition_page, name='face_recognition_page'),
    path('check_registration/', views.check_registration, name='check_registration'),
    path('register_face/', views.register_face, name='register_face'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
]
