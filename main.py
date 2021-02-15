#!/usr/bin/env python3
import yaml

from ankiconnectclient import AnkiConnectClient
from cardgenerator import CardGenerator
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

    card_generator = CardGenerator(speech_synthesizer, anki_connect_client, 'testDeck')
    card_generator.add_notes('你好')


if __name__ == '__main__':
    main()
