from connector.connector import *

def test_get_puzzle():
    puzzle = GoldenRetriver('2025-07-22')
    assert puzzle.nyjson['print_date'] == '2025-07-22'
    assert puzzle.raw == """{"status":"OK","id":811,"print_date":"2025-07-22","editor":"Wyna Liu","categories":[{"title":"SASSINESS","cards":[{"content":"ATTITUDE","position":7},{"content":"CHEEK","position":1},{"content":"LIP","position":8},{"content":"MOUTH","position":14}]},{"title":"MITIGATE","cards":[{"content":"CUSHION","position":3},{"content":"DAMPEN","position":12},{"content":"SOFTEN","position":9},{"content":"TEMPER","position":4}]},{"title":"PATTERNS","cards":[{"content":"CAMO","position":13},{"content":"CHECKERS","position":5},{"content":"HONEYCOMB","position":10},{"content":"STRIPES","position":15}]},{"title":"___ PIE","cards":[{"content":"CHESS","position":0},{"content":"CUTIE","position":11},{"content":"HUMBLE","position":6},{"content":"WHOOPIE","position":2}]}]}"""


def test_card():
    puzzle = GoldenRetriver('2025-07-22')
    solver = puzzle.unsolve()
    assert(any([(card.content == "MOUTH" and card.position == 14) for card in solver.cards]))
    assert len(solver.cards) == 16

def test_deglove_get():
    testword = 'banana'
    dg = Deglover([testword])
    assert isinstance(dg.vectors, dict)
    assert isinstance(dg.vectors[testword], np.ndarray)
    assert len(dg.vectors[testword]) == 300

def test_card_embedget():
    puzzle = GoldenRetriver('2025-07-22')
    solver = puzzle.unsolve()
    assert all([
        (len(vector) == 300) for vector in solver.embeddings.values()
    ])
