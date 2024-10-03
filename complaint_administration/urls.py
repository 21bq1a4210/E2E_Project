from django.urls import path
from complaint_administration import views

urlpatterns = [
    path('register/', views.register_complaint),
    path('', views.view_complaints),
    path('search/', views.search),
    path('escalate_complaint/', views.escalate_complaint, name='escalate_complaint'),
    path('<slug:complaint_id>/', views.view_complaint, name='view_complaint')
]