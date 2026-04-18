from twilio.twiml.voice_response import VoiceResponse

def missed_call_response():
    response = VoiceResponse()
    response.say(
        "Hi, thanks for calling Autoshine. Leave a voicemail after the tone, "
        "or hang up and we'll send you a text with a link to book online.",
        voice='Polly.Amy'
    )
    response.record(
        max_length=60,
        action='/webhooks/twilio/voicemail/',
        method='POST',
    )
    return str(response)