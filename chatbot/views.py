from django.shortcuts import render
from django.http import JsonResponse
import json
from .model_Ollama import query_with_retry

def chatbot_page(request):
    return render(request, 'chatbot.html')

def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        if user_message:
            # Call the query_with_retry function and return the result as JSON
            bot_response = query_with_retry(user_message)
            return JsonResponse({'response': bot_response}, status=200)
        return JsonResponse({'error': 'No message provided'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
