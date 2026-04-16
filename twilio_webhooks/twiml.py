from twilio.twiml.voice_response import VoiceResponse

def missed_call_response():
    response = VoiceResponse()
    response.say(
        "Hi, thanks for calling Autoshine. We're busy detailing at the moment "
        "but we've sent you a text with a link to book online. Speak soon!",
        voice='Polly.Amy'
    )
    return str(response)