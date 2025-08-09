from connector.config import *
from connector.pieces import *
import requests
import json
from datetime import datetime
import numpy as np
from db.mysql_repository import MysqlRepository as ActiveRepository
from k_means_constrained import KMeansConstrained

repo = ActiveRepository()


class Puzzle():
    def __init__(self, print_date : str = ""):

        self.fetcher = GoldenRetriever(print_date)
        nyjson = self.fetcher.nyjson

        self.status = nyjson['status']
        self.id = nyjson['id']
        self.print_date = nyjson['print_date']
        self.editor = nyjson['editor']
        self.categories = {
            category['title']: [ Card(**card) for card in category['cards'] ]
            for category in nyjson['categories']
        }
        self.cards = self._list_cards()

    def __repr__(self):
        return (
            f"------- {self.print_date}-------" +
            '\n'.join(
                ' '.join(str(card) for card in cat)
                for cat in self.categories.values()
            )
        )

    def _list_cards(self):
        return sorted(
            [card for cards in self.categories.values() for card in cards],
            key = lambda card: card.position
        )

    def store_puzzle(self):
        self.fetcher.throw_ball()

    @property
    def embeddings(self):
        return repo.retrieve_embeddings(self.cards)

    @property
    def vectordata(self):
        return np.array([v for v in self.embeddings.values()])

    def cluster(self):
        """
        """
        kmeans = KMeansConstrained(
            n_clusters = 4,
            size_min = 4,
            size_max = 4
        )
        kmeans.fit(self.vectordata)
        return kmeans.labels_


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
        """Retrieves the given date's puzzle file from New York Times.
           The file is json-formatted text.
        """
        # TODO retrieve from DB first; pull from web if not present
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except Exception as e:
            raise e
        self.raw = response.text
        self.nyjson = response.json()

    def throw_ball(self):
        raise NotImplementedError


if __name__ == '__main__':

    getter = GoldenRetriever('2025-07-22')
    j = getter.nyjson
    print(json.dumps(j))

