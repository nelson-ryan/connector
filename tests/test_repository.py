from db.mysql_repository import MysqlRepository

db = MysqlRepository()

def test_db_working():
    db.cursor.execute("select now();")
    assert db.cursor.fetchall()
