from connector.pieces import *
from connector.retriever import *
import numpy as np
from k_means_constrained import KMeansConstrained
from collections import defaultdict

class Solver():
    def __init__(self, print_date):

        self.fetcher = GoldenRetriever(print_date)
        nyjson = self.fetcher.nyjson
        self.puzzle = Puzzle(nyjson)

    @property
    def embeddings(self):
        return self.fetcher.retrieve_embeddings(self.puzzle.cards)

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
        for cluster, card in zip(clustered, self.puzzle.cards):
            solution[cluster].append(card)
        return solution



if __name__ == '__main__':
    pass
