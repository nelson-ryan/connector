## `connector`: An NYT Games Connections Solver

The objective of this project is to create an automated solver for the New York
Times daily *Connections* puzzle.  
The intended mechanism for generating the solution is to classify the words in
the puzzle using pre-trained embeddings (as of writing,
[embeddings used are from GloVe](https://nlp.stanford.edu/projects/glove/)).

The primary use case is to collect the puzzle information for a given date
and output a classification of each of the puzzles "cards."

Future developments may include:

* a UI to provide said date.
* different `Solver`s for varied approaches to calculating a solution.
* a comparison (indiviually or in aggregate) of `connector`'s success rate of
correctly-solved puzzles.


![New York Times API Logo](https://developer.nytimes.com/files/poweredby_nytimes_200c.png?v=1583354208354)

```mermaid
classDiagram
direction LR

class Repository {
    <<interface>>
    +store_puzzle(Puzzle)
    +retrieve_stored_puzzle(print_date)
    +store_solution()
    +retrieve_stored_solution()
    +retrieve_embeddings(Card[*])
}

class MysqlRepository {
    -connection
    -cursor
}

class Scraper {
    +BASEURL : str
    _get_web_puzzle(print_date) : json
}

class GoldenRetriever {
    nyjson : dict
    print_date : str

    +fetch_puzzle() : None
    _store_puzzle() : None
}

class Puzzle {
    <<datatype>>
    +status: str
    +id: int
    +print_date: str
    +editor: str
    +categories: [Card[4]]
    +cards: Card[16]
    -_list_cards() : Card[16]
}

class Solver {
    <<service>>
    -fetcher: GoldenRetriever
    +puzzle: Puzzle

    -embeddings : dict
    -vectordata : np.array[16]

    -_cluster() : float[16]
    +solve() : [Card[4]][4]

}

class Card{
    <<datatype>> 
    +content : str
    +position : int
}

class Category {
    <<datatype>> 
}


class Deglover{
    embeddingfile : Path
    words : str[16]
    vectors : dict

    _deglove() : None
    _pull_glove() : None
    _download_glovezip() : Path
    _unzip_glove() : Path
}


MysqlRepository --|>  Repository
GoldenRetriever --|> MysqlRepository
GoldenRetriever --|> Scraper
Solver *-- Puzzle

GoldenRetriever "1" --o "1" Solver 
Card "1" --o "16" Puzzle

Card "4" --o "1" Category
Category "4" --* "1" Puzzle


```
