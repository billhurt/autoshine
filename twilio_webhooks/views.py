from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .sms import send_sms
from .twiml import missed_call_response


@csrf_exempt
def missed_call(request):
    # Just plays the TwiML prompt — SMS is handled by voicemail/recording_status
    return HttpResponse(missed_call_response(), content_type='text/xml')


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


@csrf_exempt
def voicemail(request):
    recording_url = request.POST.get('RecordingUrl')
    recording_sid = request.POST.get('RecordingSid')
    from_number = request.POST.get('From')

    from twilio.rest import Client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Generate authenticated playback URL
    playback_url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Recordings/{recording_sid}.mp3"

    send_sms(
        to=settings.BUSINESS_PHONE,
        body=f"New voicemail from {from_number}. Listen: {playback_url}"
    )

    send_sms(
        to=from_number,
        body=(
            f"Hi, thanks for your voicemail! We'll call you back soon. "
            f"In the meantime you can book here: {settings.BOOKING_URL}"
        )
    )

    return HttpResponse('', content_type='text/xml')


@csrf_exempt
def call_status(request):
    status = request.POST.get('CallStatus')
    caller = request.POST.get('From')
    duration = int(request.POST.get('CallDuration', 0))
    recording_sid = request.POST.get('RecordingSid')

    print(f"CALL STATUS: {status}, DURATION: {duration}, RECORDING SID: {recording_sid}")

    # Only send SMS if hung up without leaving a voicemail
    if status == 'completed' and duration < 40 and not recording_sid:
        send_sms(
            to=caller,
            body=(
                f"Hi, sorry we missed your call! We'd love to help — "
                f"reply with what you need or book here: {settings.BOOKING_URL}"
            )
        )

    return HttpResponse('', content_type='text/xml')