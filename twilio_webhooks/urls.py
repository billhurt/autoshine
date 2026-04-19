from django.urls import path
from . import views

urlpatterns = [
    path('missed-call/', views.missed_call, name='missed_call'),
    path('incoming-sms/', views.incoming_sms, name='incoming_sms'),
    path('voicemail/', views.voicemail, name='voicemail'),
    path('recording-status/', views.recording_status, name='recording_status'),
    path('call-status/', views.call_status, name='call_status'),
]