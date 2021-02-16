#!/usr/bin/env python3

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

import sys

import yaml

from ankiconnectclient import AnkiConnectClient
from cardupdater import CardUpdater
from speechsynthesizer import SpeechSynthesizer


def parse_config_file():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <path-to-config.yaml>', file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        return yaml.full_load(f)


def main():
    config = parse_config_file()
    speech_synthesizer = SpeechSynthesizer(config['googleTextToSpeech']['apiKeyFile'],
                                           config['googleTextToSpeech']['voice']['languageCode'],
                                           config['googleTextToSpeech']['voice']['name'])
    anki_connect_client = AnkiConnectClient(config['ankiConnect']['url'])

    card_updater = CardUpdater(speech_synthesizer, anki_connect_client)
    result = card_updater.add_synthesized_speech_for_query(
        config['generator']['sourceField'],
        config['generator']['targetField'],
        config['generator']['filterQuery'],
        overwrite_target_field=config['generator'].get('overwriteTargetField', False))

    total = len(result)
    changed = [note_id for note_id in result if result[note_id]]
    unchanged = [note_id for note_id in result if not result[note_id]]

    print(f'Report: total={total} changed={len(changed)} unchanged={len(unchanged)}')
    print(f'changed: {changed}')
    print(f'unchanged: {unchanged}')


if __name__ == '__main__':
    main()
