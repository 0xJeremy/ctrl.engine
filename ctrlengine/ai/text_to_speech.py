from google.cloud import texttospeech


class text_to_speech:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US', ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL
        )
        self.audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        self.response = None

    def get_response(self):
        return self.response

    def run(self, text):
        synthesis_input = texttospeech.types.SynthesisInput(text=text)
        self.response = self.client.synthesize_speech(synthesis_input, self.voice, self.audio_config)
        return self.response

    def save_to_file(self, text, filename):
        synthesis_input = texttospeech.types.SynthesisInput(text=text)
        self.response = self.client.synthesize_speech(synthesis_input, self.voice, self.audio_config)
        with open(filename, 'wb') as out:
            out.write(self.response.audio_content)
