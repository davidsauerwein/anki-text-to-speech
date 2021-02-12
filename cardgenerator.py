from speechsynthesizer import SpeechSynthesizer


class CardGenerator:
    def __init__(self, speech_synthesizer: SpeechSynthesizer):
        self.speech_synthesizer = speech_synthesizer

    def generate(self, text):
        self.speech_synthesizer.synthesize_to_file(text, '/tmp/synthesizer_test.wav')
