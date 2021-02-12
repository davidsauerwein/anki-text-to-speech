from google.cloud import texttospeech
from google.oauth2 import service_account


# noinspection PyTypeChecker
class SpeechSynthesizer:
    def __init__(self,
                 credentials_location: str,
                 voice_language_code: str,
                 voice_name: str):
        credentials = service_account.Credentials.from_service_account_file(credentials_location)
        self.client = texttospeech.TextToSpeechClient(credentials=credentials)
        self.voice = texttospeech.VoiceSelectionParams(
            language_code=voice_language_code,
            name=voice_name
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

    def synthesize_to_file(self, text: str, filename: str) -> None:
        text_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=text_input,
            voice=self.voice,
            audio_config=self.audio_config
        )

        with open(filename, 'wb') as output_file:
            output_file.write(response.audio_content)
