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
    pass

from connector.connector import *

def test_card_embedget():
    puzzle = Puzzle('2025-07-22')
    embeddings = db.retrieve_embeddings(puzzle._list_cards())
    assert all([
        (len(vector) == 300) for vector in embeddings.values()
    ])
