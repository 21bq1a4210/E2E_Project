from django.urls import path
from user_administration import views

urlpatterns = [
    path('register_student/', views.student_registration),
    path('user_login/', views.user_login),
    path('load_classes/<path:branch>/', views.load_classes, name='load_classes')
]