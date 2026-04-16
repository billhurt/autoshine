from django.urls import path
from . import views

urlpatterns = [
    path('missed-call/', views.missed_call, name='missed_call'),
]