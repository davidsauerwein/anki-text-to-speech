from ankiconnectclient import AnkiConnectClient
from speechsynthesizer import SpeechSynthesizer


class CardUpdater:
    def __init__(self,
                 speech_synthesizer: SpeechSynthesizer,
                 anki_connect_client: AnkiConnectClient):
        self.speech_synthesizer = speech_synthesizer
        self.anki_connect_client = anki_connect_client

    def add_synthesized_speech_for_query(self,
                                         source_field: str,
                                         target_field: str,
                                         filter_query: str) -> dict:
        result = {}
        note_infos = self.anki_connect_client.get_note_infos(filter_query)
        for idx, note_info in enumerate(note_infos):
            print(f'\rProcessing note {idx + 1}/{len(note_infos)}', end='', flush=True)
            changed = self.add_synthesized_speech_to_note(source_field, target_field, note_info)
            result[note_info['noteId']] = changed
        print()
        return result

    def add_synthesized_speech_to_note(self,
                                       source_field: str,
                                       target_field: str,
                                       note_info: dict) -> bool:
        source_value = note_info['fields'][source_field]['value']
        target_value = note_info['fields'][target_field]['value']
        stripped_source = source_value.replace('\n', ' ').strip()
        media_filename = f'anki_speech_generator-{stripped_source}-{self.speech_synthesizer.voice.name}.wav'
        sound_string = f'[sound:{media_filename}]'

        # Has this note has already been processed in a previous run of this programme?
        if sound_string in target_value:
            return False

        # Is there already a synthesized version of the source_value in the database?
        if not self.anki_connect_client.media_exists(media_filename):
            data = self.speech_synthesizer.synthesize_to_base64_string(source_value)
            self.anki_connect_client.add_media(media_filename, data)

        # Update target value and tag note
        target_value = target_value + sound_string
        note_id = note_info['noteId']
        self.anki_connect_client.update_note_field(note_id, target_field, target_value)
        self.anki_connect_client.tag_note(note_id, 'anki-speech-generator')

        return True
