from twilio.twiml.voice_response import VoiceResponse

def missed_call_response():
    response = VoiceResponse()
    response.say(
        "Hi, sorry we missed your call. Please reply to the text message we’ve just sent with a few details about your request, or feel free to leave us a voicemail after the tone. "
        "Thanks for calling Autoshine",
        voice='Polly.Amy'
    )
    response.record(
        max_length=60,
        action='/webhooks/twilio/voicemail/',
        method='POST',
    )
    return str(response)