import base64

import requests


class SpeechSynthesizer:
    def __init__(self,
                 api_url: str,
                 api_key: str,
                 voice_language_code: str,
                 voice_name: str):
        self.api_url = api_url
        self.api_key = api_key
        self.voice_language_code = voice_language_code
        self.voice_name = voice_name
        self.audio_encoding = 'LINEAR16'
        self.audio_pitch = 0
        self.audio_speaking_rate = 1

    def synthesize(self, text: str) -> str:
        payload = {'audioConfig': {'audioEncoding': self.audio_encoding,
                                   'pitch': self.audio_pitch,
                                   'speakingRate': self.audio_speaking_rate},
                   'input': {'text': text},
                   'voice': {'languageCode': self.voice_language_code,
                             'name': self.voice_name}}

        r = requests.post(self.api_url,
                          params={'key': self.api_key},
                          json=payload)
        r.raise_for_status()

        reply = r.json()
        encoded_audio = reply['audioContent']

        return encoded_audio

    def decode_audio_to_file(self, encoded_audio: str, filename: str) -> None:
        if self.audio_encoding != 'LINEAR16':
            raise NotImplemented

        decoded_audio = base64.b64decode(encoded_audio)
        with open(filename, 'wb') as f:
            f.write(decoded_audio)

    def synthesize_to_file(self, text: str, filename: str) -> None:
        encoded_audio = self.synthesize(text)
        self.decode_audio_to_file(encoded_audio, filename)
