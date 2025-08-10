import numpy as np
from datetime import datetime, timedelta
from connector.connector import *
from pathlib import Path
import warnings

def validate_print_date(print_date):
    try:
        datetime.strptime(print_date, '%Y-%m-%d')
    except ValueError:
        raise Exception("Gotta be YYYY-MM-DD")
    except TypeError:
        raise Exception("Gotta be str")

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
                if any(line.startswith(word.lower()) for word in wordholder):
                    vec = line.split()
                    word = vec[0].upper()
                    if word not in wordholder:
                        continue
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

if __name__ == '__main__':

    start = '2025-07-01'
    end = datetime.strptime('2025-08-01', '%Y-%m-%d')

    words = []

    d = datetime.strptime(start, '%Y-%m-%d')
    while d < end:
        s = d.strftime('%Y-%m-%d')
        p = Puzzle(s)
        print(s)
        words += p.cards
        d += timedelta(days=1)


    deglover = Deglover([str(word) for word in words])
    deglover.embeddingfile = Path("/home/ryan/hlt/508/project/data/glove.42B.300d.txt")
    deglover._deglove()

    with open("./out.txt", "w") as f:
        for k,v in deglover.vectors.items():
            f.write(
                "('" + k + "', '" + " ".join(str(n) for n in v) + "'),\n"
            )
