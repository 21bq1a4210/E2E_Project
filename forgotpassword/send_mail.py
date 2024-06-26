from django.core.mail import send_mail
from django.conf import settings


class SentOTP:
    def __init__(self, mail_data):
        self.sender = settings.EMAIL_HOST_USER
        self.receiver = mail_data['email']
        self.subject = 'Your OTP'
        self.body = f"OTP: {mail_data['otp']}"

    def sendMail(self):
        send_mail(
            self.subject,
            self.body,
            self.sender,
            [self.receiver],
            fail_silently=False,
        )


if __name__ == "__main__":
    import django
    import os

    # Ensure Django settings are configured
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_E2E.settings')
    django.setup()

    data = {
        'email': '21bq1a4210@vvit.net',
        'otp': 12345,
    }
    SentOTP(data).sendMail()
    print('Mail sent')