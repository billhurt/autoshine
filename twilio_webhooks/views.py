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