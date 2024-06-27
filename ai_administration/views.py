import os
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.apps import apps
from openai import OpenAI
from complaint_administration.models.complaint_models import Complaint
from complaint_administration.forms.complaint_forms import complaintRegistrationForm 
from dotenv import load_dotenv

load_dotenv()
# Function prototypes for Function Calling with LLM

TOOLS = {
        "register_complaint": \
            '''
            data = dict({
                "complaint_title": str,
                "complaint_message": str,
                "type_of_complaint": str
                })

            def complaintRegistrationForm(data: dict)
                """
                Registers a complaint for the user.

                Args:
                    complaint_title (str) min 20 characters: A title for the complaint. It has to be atleast 30 characters prolong the title if needed. 
                    complaint_message (str): A meaning description for the message. Extract something from the title if not provided.
                    type_of_complaint (str): The type of complaint, It can be public or sensitive. Default value is public.
                """
                        \n
            ''',
        "user_query": \
            """\
            User Query: Question: {query}\
\ 
            Please pick a relevant function from above and fill the arguments with relevant information.\
            """
}

def get_raven_call(full_user_prompt: str):
    client = OpenAI(
        api_key=os.environ.get("API_KEY"),
        base_url="https://api.aimlapi.com"
        )

    response = client.chat.completions.create(
        model=f"{os.environ.get('MODEL_NAME')}",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant who knows everything.",
            },
            {
                "role": "user",
                "content": f"{full_user_prompt}",
            },
        ],
    )

    message = response.choices[0].message.content
    start_str = "\nCall: "
    start_idx = message.find(start_str)
    end_idx = message.find("\nThought")
    return f"{message[start_idx+len(start_str):end_idx]}"

def complaint_administration(request):
    # To be completed
    if request.method == "POST":
        user = request.user

        if not user.is_authenticated:
            return HttpResponse("Please Login before filing a complaint")

        # Getting the user model
        user_model = apps.get_model(f'user_administration.{user.role}')
        user_object = user_model.objects.get(user__id=request.user.id)
        contenttype_user_model = ContentType.objects.get_for_model(user_model)
        full_user_prompt = request.POST.get('full_user_prompt')
        full_user_prompt = TOOLS["register_complaint"] + "\n" + TOOLS["user_query"].format(query=full_user_prompt)
        print(full_user_prompt)
        call = get_raven_call(full_user_prompt)
        print(call)
        form = eval(call)
        if not form.is_valid():
            return HttpResponse("Please Enter correct details")
        
        Complaint.objects.create(user_type=contenttype_user_model, user_id=user_object.id, **form.cleaned_data)
        return HttpResponse('Complaint has been successfully registered')

    else:
        user = request.user
        if not user.is_authenticated:
            return HttpResponse("Please login")
        return render(request, "administration.html")

