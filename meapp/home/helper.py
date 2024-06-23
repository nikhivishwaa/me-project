from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

def create_user(data:dict, username:str)->User:
    user = User.objects.create_user(username=username, email=data['email'])
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.set_password(data['password'])
    user.save()
    print("User created", user)
    return user

def send_email_to_client(*email)->None:
    subject = "this is from django server testinbg team"
    message = "your opt is 9654"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = list(email)

    send_mail(subject, message, from_email, recipient_list)