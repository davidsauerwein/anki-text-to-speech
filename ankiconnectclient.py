import json
import urllib.request


class AnkiConnectClient:
    def __init__(self, url: str):
        self.url = url

    # This method is slightly modified version of the anki-connect python sample
    # https://github.com/FooSoft/anki-connect#python
    def __request(self, action: str, **params) -> dict:
        return {'action': action, 'params': params, 'version': 6}

    # This method is slightly modified version of the anki-connect python sample
    # https://github.com/FooSoft/anki-connect#python
    def invoke(self, action: str, **params):
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
