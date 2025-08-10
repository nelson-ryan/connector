from connector.config import *
from connector.pieces import *
from connector.retriever import *
import numpy as np
from k_means_constrained import KMeansConstrained
from collections import defaultdict

class Puzzle():
    def __init__(self, print_date):

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

    def __repr__(self):
        return (
            f"------- {self.print_date}-------\n" +
            '\n'.join(
                ' '.join(str(card) for card in cat)
                for cat in self.categories.values()
            )
        )

    @property
    def cards(self):
        return self._list_cards()

    def _list_cards(self):
        return sorted(
            [card for cards in self.categories.values() for card in cards],
            key = lambda card: card.position
        )

    # def store_puzzle(self):
    #     self.fetcher.throw_ball()

    @property
    def embeddings(self):
        return self.fetcher.retrieve_embeddings(self.cards)

    @property
    def vectordata(self):
        return np.array([v for v in self.embeddings.values()])

    def _cluster(self) -> np.ndarray:
        """
        Classification, returns vector of labels
        """
        kmeans = KMeansConstrained(
            n_clusters = 4,
            size_min = 4,
            size_max = 4
        )
        kmeans.fit(self.vectordata)
        return kmeans.labels_

    def solve(self) -> dict:
        solution = defaultdict(list)
        clustered = self._cluster()
        for cluster, card in zip(clustered, self.cards):
            solution[cluster].append(card)
        return solution



if __name__ == '__main__':

    getter = GoldenRetriever('2025-07-22')
    j = getter.nyjson

