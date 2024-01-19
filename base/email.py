from django.core.mail import send_mail
from django.conf import settings

def send_account_activation_email(email, email_token):
    subject = 'Your Accounts need to be varified!'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on the link to activate your account http://127.0.0.1:8000/account/activate/{email_token}'
    send_mail(subject,message,email_from, [email], fail_silently=False)


def send_welcome_email(user):
     send_mail(
        "Welcome To ShoeStore",
        "We are glad to welcome you to our Store",
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )
