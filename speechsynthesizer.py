#  Copyright (c) 2021 David Sauerwein
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

import base64

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
