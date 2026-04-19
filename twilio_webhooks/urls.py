from django.urls import path
from . import views

urlpatterns = [
    path('missed-call/', views.missed_call, name='missed_call'),
    path('recording-status/', views.recording_status, name='recording_status'),
    path('voicemail/', views.voicemail, name='voicemail'),
    path('incoming-sms/', views.incoming_sms, name='incoming_sms'),
    path('call-status/', views.call_status, name='call_status'),
    path('voicemail/play/<str:recording_sid>/', views.play_voicemail, name='play_voicemail'),
]