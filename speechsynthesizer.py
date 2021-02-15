import base64
from typing import IO

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

    def synthesize(self, text: str) -> texttospeech.SynthesizeSpeechResponse:
        text_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=text_input,
            voice=self.voice,
            audio_config=self.audio_config
        )

        return response

    def synthesize_to_base64_string(self, text: str) -> str:
        response = self.synthesize(text)
        return base64.b64encode(response.audio_content).decode('utf-8')

    def synthesize_to_file(self, text: str, output_file: IO) -> None:
        response = self.synthesize(text)
        output_file.write(response.audio_content)

    def synthesize_to_filename(self, text: str, filename: str) -> None:
        with open(filename, 'wb') as output_file:
            self.synthesize_to_file(text, output_file)
