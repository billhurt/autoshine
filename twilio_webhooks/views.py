from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .sms import send_sms
from .twiml import missed_call_response

@csrf_exempt
def missed_call(request):
    caller = request.POST.get('From')
    
    if caller:
        send_sms(
            to=caller,
            body=(
                f"Hi, sorry we missed your call! We'd love to help — "
                f"tell us what you need and book directly here: {settings.BOOKING_URL}"
            )
        )
    
    return HttpResponse(missed_call_response(), content_type='text/xml')


@csrf_exempt
def incoming_sms(request):
    from_number = request.POST.get('From')
    message_body = request.POST.get('Body')
    
    # Forward the reply to the business owner
    send_sms(
        to=settings.BUSINESS_PHONE,
        body=f"Reply from {from_number}: {message_body}"
    )
    
    # Auto-reply to the customer
    from twilio.twiml.messaging_response import MessagingResponse
    response = MessagingResponse()
    response.message(
        "Thanks for getting in touch! We'll get back to you as soon as we can."
    )
    return HttpResponse(str(response), content_type='text/xml')