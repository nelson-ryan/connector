import requests
import json
from datetime import datetime


class Card():
    def __init__(self, content : str, position : int):
        self.content = content
        self.position = position


class Solver():
    def __init__(self, cards : list[Card]):
        self.cards = cards


class GoldenRetriever():
    BASEURL = "http://www.nytimes.com/svc/connections/v2/"

    def __init__(self, print_date:str):
        self.nyjson : dict
        self.print_date = print_date
        try:
            datetime.strptime(self.print_date, '%Y-%m-%d')
        except ValueError:
            raise Exception("Gotta be YYYY-MM-DD")
        except TypeError:
            raise Exception("Gotta be str")
        self.url = self.BASEURL + print_date + ".json"
        self._get_puzzle()

    def _get_puzzle(self):
        # TODO retrieve from DB first
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except Exception as e:
            raise e
        self.raw = response.text
        self.nyjson = response.json()

    def unsolve(self) -> Solver:
        return


if __name__ == '__main__':

    getter = GoldenRetriever('2025-07-20')
    j = getter.nyjson
    print(json.dumps(j))

    [
    card['content']
    for category in j['categories']
    for card in category['cards']
    ]
