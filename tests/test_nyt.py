from connector.connector import *
from utils.utils import *

gr = GoldenRetriever('2025-07-22')
puzzle = Puzzle(gr.nyjson)


def test_retrieve():
    assert isinstance(gr.nyjson, dict)
    assert gr.nyjson['print_date'] == '2025-07-22'
    assert gr.nyjson['editor'] == 'Wyna Liu'
    assert len(gr.nyjson['categories']) == 4

def test_puzzle():
    assert puzzle.status == "OK"
    assert puzzle.editor == "Wyna Liu"
    assert(any(
        (card.content == "MOUTH" and card.position == 14)
        for cardlist in puzzle.categories.values()
        for card in cardlist
    ))

def test_deglove_get():
    testword = 'banana'
    dg = Deglover([testword])
    assert isinstance(dg.vectors, dict)
    assert isinstance(dg.vectors[testword], np.ndarray)
    assert len(dg.vectors[testword]) == 300

def test_cardlist():
    cl = puzzle._list_cards()
    assert isinstance(cl, list)
