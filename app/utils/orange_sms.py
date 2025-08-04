# utils/orange_sms.py

import requests
import json
from django.conf import settings

def get_access_token():
    url = "https://api.orange.com/oauth/v3/token"
    headers = {'Authorization': f"Basic {settings.ORANGE_API_BASIC}", 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, headers=headers, data=data)
    return response.json()['access_token']

def envoyer_sms(numero, message):
    token = get_access_token()
    url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B24300000000/requests"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "outboundSMSMessageRequest": {
            "address": f"tel:+243{numero}",  # Sans le premier 0
            "senderAddress": "tel:+24300000000",  # Ton numéro Orange validé
            "outboundSMSTextMessage": {"message": message}
        }
    }
    response = requests.post(url, headers=headers, json=data)
