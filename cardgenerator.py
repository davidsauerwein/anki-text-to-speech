from speechsynthesizer import SpeechSynthesizer


class CardGenerator:
    def __init__(self, speech_synthesizer: SpeechSynthesizer):
        self.speech_synthesizer = speech_synthesizer

    def generate(self, text):
        encoded_audio = self.speech_synthesizer.synthesize(text)
        self.speech_synthesizer.decode_audio_to_file(encoded_audio, '/tmp/synthesizer_test.wav')
