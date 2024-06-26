# views.py
from django.shortcuts import render
from django.http import JsonResponse
import json
from .gemini_model import chat  # Adjust the import according to your project structure

def chatbot_page(request):
    return render(request, 'chatbot.html')

def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        if user_message:
            bot_response = chat(user_message)
            return JsonResponse({'response': bot_response}, status=200)
        return JsonResponse({'error': 'No message provided'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
