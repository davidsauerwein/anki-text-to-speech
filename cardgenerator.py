from ankiconnectclient import AnkiConnectClient
from speechsynthesizer import SpeechSynthesizer


class CardGenerator:
    def __init__(self,
                 speech_synthesizer: SpeechSynthesizer,
                 anki_connect_client: AnkiConnectClient,
                 deck: str):
        self.speech_synthesizer = speech_synthesizer
        self.anki_connect_client = anki_connect_client
        self.deck = deck
        self.create_deck()

    def create_deck(self) -> None:
        # This will not override an existing deck according to docs
        self.anki_connect_client.invoke('createDeck', deck=self.deck)

    def add_notes(self, text: str) -> None:
        # TODO for now we will store the data in a tmp file an pass the location of that file through the api
        # What we really want is to pass the data base64 encoded. The API does not allow that at the moment
        file_name = f'anki-speech-generator-{text}'
        encoded_audio = self.speech_synthesizer.synthesize_to_base64_string(text)
        note = {
            'deckName': self.deck,
            'modelName': 'Basic',  # TODO
            'fields': {
                'Front': 'Write Pinyin and Character for the given audio',
                'Back': text
            },
            'options': {
                'allowDuplicate': False,
                'duplicateScope': 'deck',
                'duplicateScopeOptions': {
                    'deckName': self.deck,
                    'checkChildren': False
                }
            },
            'tags': ['anki-speech-generator'],
            'audio': [{
                'data': encoded_audio,
                'filename': file_name,
                'fields': [
                    'Front',
                    'Back'
                ]
            }]
        }

        self.anki_connect_client.invoke('addNote', note=note)

    def generate(self, text) -> None:
        self.speech_synthesizer.synthesize_to_filename(text, '/tmp/synthesizer_test.wav')
