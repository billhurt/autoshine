from twilio.rest import Client
from django.conf import settings

def send_sms(to, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=to,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=body
    )