from db.mysql_repository import MysqlRepository

db = MysqlRepository()

def test_db_working():
    db.cursor.execute("select now();")
    assert db.cursor.fetchall()

def test_retrieve_embeddings():
    words = ['stripes', 'cushion']
    res = db.retrieve_embeddings(words)
    toks = [r[0] for r in res]
    assert all(w in toks for w in words)
