from connector.connector import *



gr = GoldenRetriever('2025-07-22')
puzzle = gr.puzzle()


def test_makedata():
    data = puzzle.vectordata
    assert(data.shape == (16, 300))

def test_cluster():
    c = puzzle.cluster()
    assert(len(c) == 16)
    for i in range(4):
        assert(len([x for x in c if x == i]) == 4)

