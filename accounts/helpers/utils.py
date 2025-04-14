from django.core.mail import send_mail
from django.conf import settings
from accounts.helpers.otp_client import send_otp_email
import datetime as dt
import random as rd

def send_email_to_client(subject, message, *email)->None:
    from_email = settings.EMAIL_HOST_USER
    recipient_list = list(email)

    send_mail(subject, message, from_email, recipient_list)

def otp_helper(user):
    user.email_otp = f"{rd.randint(10, 99)}{rd.randint(10, 99)}{rd.randint(10, 99)}"
    user.otp_timestamp = dt.datetime.now(dt.timezone.utc)
    send_otp_email(user.email, user.first_name, user.email_otp)
    user.save()

def forgot_otp_helper(user):
    user.forgot_password_otp = f"{rd.randint(10, 99)}{rd.randint(10, 99)}{rd.randint(10, 99)}"
    user.forgot_otp_timestamp = dt.datetime.now(dt.timezone.utc)
    send_otp_email(user.email, user.first_name, user.forgot_password_otp, reason='Forgot Password')
    user.save()
