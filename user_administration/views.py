from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from user_administration.forms import student_forms
from .escalation_models import Role
from .models import CustomUser, Student, Class
from django.contrib.auth import authenticate, login
from django.contrib import messages


def student_registration(request):
    if request.method == "POST":
        form = student_forms.studentRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user_details = {
                'username': form.cleaned_data['username'],
                'role': Role.objects.get(role='Student'),
                'image': form.cleaned_data['image'],
                'password': form.cleaned_data['password']
            }

            user = CustomUser(**user_details)

            user.set_password(form.cleaned_data['password'])
            try:
                user.full_clean()
                user.save()

                student_details = {
                    'roll_no': form.cleaned_data['roll_no'].lower(),
                    'branch': form.cleaned_data['branch'],
                    'class_room': form.cleaned_data['class_room'],
                    'year': form.cleaned_data['year'],
                }
                student = Student(**student_details, user=user)
                student.full_clean()
                student.save()

            except ValidationError as e:
                return HttpResponse(str(e.messages))

            student = Group.objects.get(name='Student')
            user.groups.add(student)
            messages.success(request, "Registration Successful")
            return HttpResponseRedirect('/user_administration/user_login/')
        else:
            return HttpResponse("The data is not clean")
    else:
        form = student_forms.studentRegistrationForm()
        return render(request, 'user_administration/student_registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = student_forms.studentLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, "You are logged in")
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponse("Invalid username or password")

    else:
        form = student_forms.studentLoginForm()
        return render(request, 'user_administration/user_login.html', {'form': form})


def load_classes(request, branch):
    classes = Class.objects.filter(branch_id=branch)
    return render(request, 'user_administration/load_classes.html', {'classes': classes})
