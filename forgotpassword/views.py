import random
import socket
import string

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

from forgotpassword.send_mail import SentOTP

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def generate_and_send_otp(user, email):
    otp = generate_otp()  # Replace with the new OTP generation method

    mail_data = {
        'email': email,
        'otp': otp
    }
    try:
        mailer = SentOTP(mail_data)
        mailer.sendMail()
        return otp  # Directly return OTP, handle session outside
    except socket.gaierror as e:
        print(f"Socket error: {e}")
        raise Exception("A network error occurred while sending the email. Please check your internet connection.")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise Exception("An error occurred while sending the email. Please try again later.")

def forgotpassword(request):
    stage = 'email'  # Initial stage

    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST['email']
            try:
                user = User.objects.get(email=email)
                otp = generate_and_send_otp(user, email)
                request.session['otp'] = otp
                request.session['email'] = email
                stage = 'otp'
                messages.success(request, 'OTP has been sent to your email.')
            except User.DoesNotExist:
                stage = 'email'
                messages.error(request, 'No account found with this email address.')
            except Exception as e:
                stage = 'email'
                messages.error(request, str(e))

        elif 'otp' in request.POST:
            otp_input = request.POST['otp']
            otp = request.session.get('otp')
            if otp and otp_input == otp:
                stage = 'password'
                messages.success(request, 'OTP verified successfully. Please enter a new password.')
            else:
                stage = 'otp'
                messages.error(request, 'Invalid OTP. Please try again.')

        elif 'new_password1' in request.POST and 'new_password2' in request.POST:
            email = request.session.get('email')
            new_password1 = request.POST['new_password1']
            new_password2 = request.POST['new_password2']
            if new_password1 == new_password2:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, 'Password changed successfully. Please log in with your new password.')
                    return redirect('login')
                except User.DoesNotExist:
                    stage = 'password'
                    messages.error(request, 'An error occurred while changing the password. Please try again.')
            else:
                stage = 'password'
                messages.error(request, 'Passwords do not match. Please try again.')

    return render(request, 'forgotpassword.html', {'stage': stage})