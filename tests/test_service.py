from connector.connector import *


puzzle = Puzzle('2025-07-22')


def test_makedata():
    data = puzzle.vectordata
    assert(data.shape == (16, 300))

def test_cluster():
    c = puzzle._cluster()
    assert(len(c) == 16)
    for i in range(4):
        assert(len([x for x in c if x == i]) == 4)

def test_mappings():
    for (word, emb), vec1 in zip(puzzle.embeddings.items(), puzzle.vectordata):
        print(word, emb[0], vec1[0])
        assert(emb[0] == vec1[0])

def test_solve():
    solution = puzzle.solve()
    assert(len(solution) == 4)
    for label, category in solution.items():
        assert(len(category) == 4)
    print(*[(int(k), v) for k, v in solution.items()], sep = "\n")
