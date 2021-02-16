#!/usr/bin/env python3
import yaml

from ankiconnectclient import AnkiConnectClient
from cardupdater import CardUpdater
from speechsynthesizer import SpeechSynthesizer


# TODO setup.py
# TODO license
# TODO pip requirements
# TODO tests
# TODO docs

def parse_config_file(filename):
    with open(filename) as f:
        return yaml.full_load(f)


def main():
    config = parse_config_file('config.yaml')
    speech_synthesizer = SpeechSynthesizer(config['credentials_location'],
                                           config['voice']['languageCode'],
                                           config['voice']['name'])
    anki_connect_client = AnkiConnectClient('http://localhost:8765')

    card_updater = CardUpdater(speech_synthesizer, anki_connect_client)
    query = 'deck:Chinese_1'
    result = card_updater.add_synthesized_speech_for_query('Word (Character)', 'Generated Speech', query)

    total = len(result)
    changed = [note_id for note_id in result if result[note_id]]
    unchanged = [note_id for note_id in result if not result[note_id]]

    print(f'Report: total={total} changed={len(changed)} unchanged={len(unchanged)}')
    print(f'changed: {changed}')
    print(f'unchanged: {unchanged}')


if __name__ == '__main__':
    main()
