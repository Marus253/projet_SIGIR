# app/utils/notifications.py

from django.core.mail import send_mail
from django.conf import settings

def envoyer_email_relance(email, sujet, message):
    send_mail(
        sujet,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

