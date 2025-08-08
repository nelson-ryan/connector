from connector.config import *
import requests
import json
from datetime import datetime
import numpy as np
from pathlib import Path
import warnings
from db.mysql_repository import MysqlRepository as ActiveRepository
from k_means_constrained import KMeansConstrained

repo = ActiveRepository()

class Card():
    """Contains a given word's info as listed in the NYT 'card' entries.
       Named for how each word is presented in the game, i.e. on cards.
    """
    def __init__(self, content : str, position : int):
        self.content = content
        self.position = position

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content

class Category():
    def __init__(self):
        pass


class Puzzle():
    def __init__(self,
                 status : str = "",
                 id : str = "",
                 print_date : str = "",
                 editor : str = "",
                 categories : list = []
    ):
        self.status = status
        self.id = id
        self.print_date = print_date
        self.editor = editor
        self.categories = {
            category['title']: [ Card(**card) for card in category['cards'] ]
            for category in categories
        }
        self.cards = sorted(
            [card for cards in self.categories.values() for card in cards],
            key = lambda card: card.position
        )

    def store_puzzle(self):
        raise NotImplementedError

    def _list_cards(self):
        return [
            card.content
            for cards in self.categories.values()
            for card in cards
        ]

    @property
    def embeddings(self):
        return repo.retrieve_embeddings(self.cards)

    @property
    def vectordata(self):
        return np.array([v for v in self.embeddings.values()])

    def cluster(self):
        kmeans = KMeansConstrained(
            n_clusters = 4,
            size_min = 4,
            size_max = 4
        )
        kmeans.fit(self.vectordata)
        return kmeans.labels_


class Deglover():
    """Accesses the GloVe embedding file and retrieves only the
       relevant words' vectors.
       Because this requires the massive GloV embeddings files, this may be
       best left out.
    """
    def __init__(self, words : list = []):
        self.embeddingfile = Path(EMBEDDINGPATH)
        self.words = words
        self.vectors = {word : np.zeros(DIMENSIONS) for word in self.words}
        self._deglove()

    def _deglove(self):
        """Extracts relevant embeddings from a locally-saved embeddings file
           and assigns them to the object attribute self.vectors
        """
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

    def _pull_glove(self):
        """What to do if the embeddings file is not already local.
        """
        self._download_glovezip()
        self._unzip_glove()

    def _download_glovezip(self):
        """Downloads embeddings from Stanford and saves locally.
           Not super ideal, but here it is.
           Perhaps this can be changed to some kind of remote lookup, but
           obviously the zip download file is no good for that.
        """
        if not self.embeddingfile.parent.exists():
            warnings.warn("You're about to download a sizeable file, boy howdy!")
            self.embeddingfile.parent.mkdir(parents = True)
        zipfile = GLOVEURL.split('/')[-1]
        try:
            with requests.get(GLOVEURL, stream = True) as stream:
                with open(zipfile, 'wb') as zip:
                    for chunk in stream.iter_content():
                        zip.write(chunk)
        except Exception as e:
            raise e
        self.zipfile = zipfile

    def _unzip_glove(self):
        # TODO
        raise NotImplementedError

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

    def puzzle(self):
        return Puzzle(**self.nyjson)

if __name__ == '__main__':

    getter = GoldenRetriever('2025-07-22')
    j = getter.nyjson
    print(json.dumps(j))

