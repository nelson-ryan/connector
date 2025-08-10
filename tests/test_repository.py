from db.mysql_repository import MysqlRepository as ActiveRepository

db = ActiveRepository()

def test_db_working():
    db.cursor.execute("select now();")
    assert db.cursor.fetchall()

def test_retrieve_embeddings():
    words = ['stripes', 'cushion']
    res = db.retrieve_embeddings(words)
    assert len(words) == len(res)
    assert all(w in res.keys() for w in words)

def test_retrieve_stored_puzzle():
    d = '2025-07-02'
    gotem = db.retrieve_stored_puzzle(d)
    assert(isinstance(gotem, dict))
    assert(gotem['print_date'] == d)
    assert(gotem['editor'] == 'Jon Do')
    assert(len(gotem['categories']) == 4)
    assert(all(len(c) == 4 for c in gotem['categories'].values()))
    # TODO this does not mirror nyjsonjj

from connector.connector import *
puzzle = Puzzle('2025-07-22')

def test_card_embedget():
    embeddings = db.retrieve_embeddings(puzzle._list_cards())
    assert all([
        (len(vector) == 300) for vector in embeddings.values()
    ])

def test_card_embedget_from_Puzzle():
    embeddings = puzzle.embeddings
    assert all([
        (len(vector) == 300) for vector in embeddings.values()
    ])
