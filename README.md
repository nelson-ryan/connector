## `connector`: An NYT Games Connections Solver


```mermaid
classDiagram

class GoldenRetriever {
    <<datatype>> 
    nyjson : dict
    print_date : str

    _get_puzzle() : None
    _store_puzzle() : None
    unsolve() : Solver
}

class Card{
    <<datatype>> 
    +content : str
    +position : int
}

class Solver{
    <<datatype>> 
    cards : Card[4]
    deglover : Deglover

    _cosim(a : ndarray, b : ndarray) : float
    solve() : [Card[4]][4]
}


class Deglover{
    <<datatype>> 
    embeddingfile : Path
    words : str[16]
    vectors : dict

    _deglove() : None
    _pull_glove() : None
    _download_glovezip() : Path
    _unzip_glove() : Path
}

GoldenRetriever "1" --> "1" Solver : generates
Deglover --* Solver
Card "1" --o "16" Deglover
Card "1" --o "16" Solver
