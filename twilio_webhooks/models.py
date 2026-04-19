from django.db import models

class VoicemailRecord(models.Model):
    call_sid = models.CharField(max_length=64, unique=True)
    from_number = models.CharField(max_length=20)
    recording_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)