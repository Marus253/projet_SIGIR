# app/tasks.py

#from celery import shared_task
from celery import shared_task
from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Infraction
from utils.orange_sms import envoyer_sms

@shared_task
def relancer_usagers():
    today = now()
    infractions = Infraction.objects.filter(est_payee=False, date_limite__lt=today)

    for inf in infractions:
        message = f"Bonjour, vous avez une amende de {inf.montant} FC non payée. Merci de régulariser rapidement pour éviter des sanctions."
        
        # Envoi email
        if inf.usager.email:
            send_mail(
                subject="[Infraction Routière] Relance de paiement",
                message=message,
                from_email=None,
                recipient_list=[inf.usager.email],
                fail_silently=True
            )
        
        # Envoi SMS
        if inf.usager.telephone:
            envoyer_sms(inf.usager.telephone, message)
