from connector.connector import *



puzzle = Puzzle('2025-07-22')


def test_makedata():
    data = puzzle.vectordata
    assert(data.shape == (16, 300))

def test_cluster():
    c = puzzle.cluster()
    assert(len(c) == 16)
    for i in range(4):
        assert(len([x for x in c if x == i]) == 4)

