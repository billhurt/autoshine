from django.shortcuts import render
from datetime import date

def booking(request):
    return render(request, 'booking.html', {
        'today': date.today().isoformat()
    })