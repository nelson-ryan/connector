from connector import *
import requests
import json
from datetime import datetime
import numpy as np

class Card():
    """Contains a given word's info as listed in the NYT 'card' entries.
       Named for how each word is presented in the game, i.e. on cards.
    """
    def __init__(self, content : str, position : int):
        self.content = content
        self.position = position

    def retrieve_embedding(self):
        raise NotImplementedError


class Solver():
    def __init__(self, cards : list[Card]):
        self.cards = cards
        self.deglover = Deglover([card.content for card in self.cards])
        self.embeddings = self.deglover.vectors # feels sloppy to duplicate

    @staticmethod
    def _pnorm(a, p = 2):
        return np.power((sum(np.power(a,p))), (1/p))

    @staticmethod
    def _cosim(a, b):
        numer = np.dot(a, b)
        denom = Solver._pnorm(a)*Solver._pnorm(b)
        return numer / denom

    def solve(self):
        raise NotImplementedError


class Deglover():
    """Accesses the GloVe embedding file and retrieves only the
       relevant words' vectors.
    """
    def __init__(self, words : list):
        self.embeddingfile = EMBEDDINGPATH
        self.words = words
        self.vectors = {word : np.zeros(DIMENSIONS) for word in self.words}
        self._deglove()

    def _deglove(self):
        wordholder = self.words.copy()
        # TODO move embeddings to a DB or pickle or something;
        # this can take a lot of seconds to run
        with open(self.embeddingfile) as file:
            while (
                ( line := file.readline() ) and wordholder
           ):
                if any(line.startswith(word) for word in self.words):
                    vec = line.split()
                    word = vec[0]
                    self.vectors[word] = np.array(vec[1:])
                    wordholder.remove(word)
        return None


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
        # TODO retrieve from DB first; pull from web if not present
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except Exception as e:
            raise e
        self.raw = response.text
        self.nyjson = response.json()

    def _store_puzzle(self):
        raise NotImplementedError

    def unsolve(self) -> Solver:
        cards = [
            Card(content = card['content'], position = card['position'])
            for category in self.nyjson['categories']
            for card in category['cards']
        ]
        return Solver(cards = cards)


if __name__ == '__main__':

    getter = GoldenRetriever('2025-07-20')
    j = getter.nyjson
    print(json.dumps(j))

