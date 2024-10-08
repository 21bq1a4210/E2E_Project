# all_urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('chatbot/', views.chatbot_page, name='chatbot_page'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),
    # path("", include("dashboard.urls")),
]