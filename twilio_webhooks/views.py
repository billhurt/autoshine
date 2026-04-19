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
    from_number = request.POST.get('From')

    # Notify business owner
    send_sms(
        to=settings.BUSINESS_PHONE,
        body=f"New voicemail from {from_number}: {recording_url}.mp3"
    )

    # Thank the customer
    send_sms(
        to=from_number,
        body=(
            f"Hi, thanks for your voicemail! We'll call you back soon. "
            f"In the meantime you can book here: {settings.BOOKING_URL}"
        )
    )

    return HttpResponse('', content_type='text/xml')


@csrf_exempt
def recording_status(request):
    status = request.POST.get('RecordingStatus')
    caller = request.POST.get('From')
    
    # Log everything Twilio sends so we can see what's coming through
    print(f"RECORDING STATUS: {status}")
    print(f"CALLER: {caller}")
    print(f"ALL POST DATA: {dict(request.POST)}")

    if status == 'no-recording':
        send_sms(
            to=caller,
            body=(
                f"Hi, sorry we missed your call! We'd love to help — "
                f"reply with what you need or book here: {settings.BOOKING_URL}"
            )
        )

    return HttpResponse('', content_type='text/xml')


@csrf_exempt
def call_status(request):
    status = request.POST.get('CallStatus')
    caller = request.POST.get('From')
    duration = int(request.POST.get('CallDuration', 0))
    recording_url = request.POST.get('RecordingUrl')

    # Only send SMS if call ended with no recording and short duration
    if status == 'completed' and duration < 25 and not recording_url:
        send_sms(
            to=caller,
            body=(
                f"Hi, sorry we missed your call! We'd love to help — "
                f"reply with what you need or book here: {settings.BOOKING_URL}"
            )
        )

    return HttpResponse('', content_type='text/xml')