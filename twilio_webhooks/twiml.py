from twilio.twiml.voice_response import VoiceResponse

def missed_call_response():
    response = VoiceResponse()
    response.say(
        "Hi, sorry we missed your call. Please reply to the text message we’ve just sent, or feel free to leave a voicemail after the tone. "
        "Thanks for calling Outcast detailing.",
        voice='Polly.Amy'
    )
    response.record(
        max_length=60,
        action='/webhooks/twilio/voicemail/',
        method='POST',
        recording_status_callback='https://web-production-79971.up.railway.app/webhooks/twilio/recording-status/',
        recording_status_callback_method='POST',
        recording_status_callback_event='in-progress',
    )
    return str(response)