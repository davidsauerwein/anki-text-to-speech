#!/usr/bin/env python3
import yaml

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
    speech_synthesizer = SpeechSynthesizer(config['apiUrl'],
                                           config['apiKey'],
                                           config['voice']['languageCode'],
                                           config['voice']['name'])

    card_generator = CardGenerator(speech_synthesizer)
    card_generator.generate('test')


if __name__ == '__main__':
    main()
