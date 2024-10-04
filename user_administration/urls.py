from django.urls import path
from user_administration import views

app_name = 'user_administration'

urlpatterns = [
    path('register_student/', views.student_registration, name='register'),
    path('user_login/', views.user_login, name='login'),
    path('load_classes/<path:branch>/', views.load_classes, name='load_classes')
]
