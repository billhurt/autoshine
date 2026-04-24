import requests
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.conf import settings
from requests.auth import HTTPBasicAuth
from .sms import send_sms
from .twiml import missed_call_response


@csrf_exempt
def missed_call(request):
    return HttpResponse(missed_call_response(), content_type='text/xml')


@csrf_exempt
def recording_status(request):
    call_sid = request.POST.get('CallSid')
    status = request.POST.get('RecordingStatus')
    caller = request.POST.get('From')

    if status == 'in-progress':
        send_sms(
            to=caller,
            body=(
                f"Hi, Outkast detailing here, sorry we missed your call! We'd love to help — "
                f"reply with what you need or book here: {settings.BOOKING_URL}"
            )
        )

    return HttpResponse('', content_type='text/xml')


@csrf_exempt
def voicemail(request):
    recording_sid = request.POST.get('RecordingSid')
    from_number = request.POST.get('From')

    if recording_sid:
        # They left a voicemail
        playback_url = f"https://web-production-79971.up.railway.app/webhooks/twilio/voicemail/play/{recording_sid}/"
        send_sms(
            to=settings.BUSINESS_PHONE,
            body=f"New voicemail from {from_number}. Listen: {playback_url}"
        )
        send_sms(
            to=from_number,
            body=(
                f"Hi, Outkast detailing here, thanks for your voicemail! We'll call you back soon. "
                f"In the meantime you can book here: {settings.BOOKING_URL}"
            )
        )
    else:
        # They hung up without leaving a voicemail
        send_sms(
            to=from_number,
            body=(
                f"Hi, Outkast detailing here, sorry we missed your call! We'd love to help — "
                f"reply with what you need or book here: {settings.BOOKING_URL}"
            )
        )

    return HttpResponse('', content_type='text/xml')


@csrf_exempt
def incoming_sms(request):
    from_number = request.POST.get('From')
    message_body = request.POST.get('Body')

    send_sms(
        to=settings.BUSINESS_PHONE,
        body=f"Reply from {from_number}: {message_body}"
    )

    from twilio.twiml.messaging_response import MessagingResponse
    response = MessagingResponse()
    response.message("Thanks for your message! We'll get back to you as soon as we can.")
    return HttpResponse(str(response), content_type='text/xml')


def play_voicemail(request, recording_sid):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Recordings/{recording_sid}.mp3"
    r = requests.get(
        url,
        auth=HTTPBasicAuth(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
        stream=True
    )
    return StreamingHttpResponse(r.iter_content(chunk_size=8192), content_type='audio/mpeg')