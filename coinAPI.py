import requests
import json


class CoinAPI:

    def __init__(self, url, api_key, token_from, token_to):
        self.token_from = token_from
        self.token_to = token_to
        self.headers = {'X-CoinAPI-Key': api_key}
        self.url = url + token_from + "/" + token_to

    def get_currency(self):
        return requests.get(self.url, headers=self.headers)

    def get_dict_response(self):
        return json.loads(self.get_currency().text)
