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
                                         filter_query: str,
                                         overwrite_target_field: bool = False) -> dict:
        result = {}

        note_infos = self.anki_connect_client.get_note_infos(filter_query)
        for idx, note_info in enumerate(note_infos):
            print(f'\rProcessing note {idx + 1}/{len(note_infos)}', end='', flush=True)
            changed = self.add_synthesized_speech_to_note(source_field,
                                                          target_field,
                                                          note_info,
                                                          overwrite_target_field=overwrite_target_field)
            result[note_info['noteId']] = changed
        print()

        return result

    def add_synthesized_speech_to_note(self,
                                       source_field: str,
                                       target_field: str,
                                       note_info: dict,
                                       overwrite_target_field: bool = False) -> bool:
        source_value = note_info['fields'][source_field]['value']
        target_value = note_info['fields'][target_field]['value']
        stripped_source = source_value.replace('\n', ' ').strip()
        media_filename = f'anki-text-to-speech{stripped_source}-{self.speech_synthesizer.voice.name}.wav'
        sound_string = f'[sound:{media_filename}]'

        # Is there already a synthesized version of the source_value in the database?
        if not self.anki_connect_client.media_exists(media_filename):
            data = self.speech_synthesizer.synthesize_to_base64_string(source_value)
            self.anki_connect_client.add_media(media_filename, data)

        # Has this note already been processed in a previous run?
        if overwrite_target_field:
            if sound_string == target_value:
                return False
            target_value = sound_string
        else:
            if sound_string in target_value:
                return False
            target_value = target_value + sound_string

        # Update target field and tag note
        note_id = note_info['noteId']
        self.anki_connect_client.update_note_field(note_id, target_field, target_value)
        self.anki_connect_client.tag_note(note_id, 'anki-text-to-speech')

        return True
