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

import json
import urllib.request
from typing import List


class AnkiConnectClient:
    def __init__(self, url: str):
        self.url = url

    # This method is slightly modified version of the anki-connect python sample
    # https://github.com/FooSoft/anki-connect#python
    def __request(self, action: str, **params) -> dict:
        return {'action': action, 'params': params, 'version': 6}

    # This method is slightly modified version of the anki-connect python sample
    # https://github.com/FooSoft/anki-connect#python
    def __invoke(self, action: str, **params):
        request_json = json.dumps(self.__request(action, **params)).encode('utf-8')
        response = json.load(urllib.request.urlopen(urllib.request.Request(self.url, request_json)))
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']

    def get_note_infos(self, query: str) -> List[dict]:
        note_ids = self.__invoke('findNotes', query=query)
        return self.__invoke('notesInfo', notes=note_ids)

    def media_exists(self, filename: str) -> bool:
        result = self.__invoke('retrieveMediaFile', filename=filename)
        return result is not False

    def add_media(self, filename: str, data: str) -> None:
        self.__invoke('storeMediaFile', filename=filename, data=data)

    def update_note_field(self, note_id: int, field: str, value) -> None:
        note = {'id': note_id,
                'fields': {
                    field: value
                }}
        self.__invoke('updateNoteFields', note=note)

    def tag_note(self, note_id: int, tag: str) -> None:
        self.__invoke('addTags', notes=[note_id], tags=tag)
