from connector.connector import *

gr = GoldenRetriever('2025-07-22')


def test_retrieve():
    assert isinstance(gr.nyjson, dict)
    assert gr.nyjson['print_date'] == '2025-07-22'
    assert gr.raw == """{"status":"OK","id":811,"print_date":"2025-07-22","editor":"Wyna Liu","categories":[{"title":"SASSINESS","cards":[{"content":"ATTITUDE","position":7},{"content":"CHEEK","position":1},{"content":"LIP","position":8},{"content":"MOUTH","position":14}]},{"title":"MITIGATE","cards":[{"content":"CUSHION","position":3},{"content":"DAMPEN","position":12},{"content":"SOFTEN","position":9},{"content":"TEMPER","position":4}]},{"title":"PATTERNS","cards":[{"content":"CAMO","position":13},{"content":"CHECKERS","position":5},{"content":"HONEYCOMB","position":10},{"content":"STRIPES","position":15}]},{"title":"___ PIE","cards":[{"content":"CHESS","position":0},{"content":"CUTIE","position":11},{"content":"HUMBLE","position":6},{"content":"WHOOPIE","position":2}]}]}"""

def test_puzzle():
    puzzle = gr.puzzle()
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
    puzzle = gr.puzzle()
    cl = puzzle._list_cards()
    assert isinstance(cl, list)
