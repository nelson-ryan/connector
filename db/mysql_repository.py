from db.repository import Repository
import mysql.connector


class MysqlRepository(Repository):

    def __init__(self):
        super().__init__()
        config = {
            'user': 'root',
            'password': 'woof',
            'host': '127.0.0.1', # 'mysql',  # When you run this on your machine change it to 'localhost'
            'port': '32000', # '3306',  # When you run this on your machine change it to '32000'
            'database': 'connector'
        }
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()


    def store_puzzle(self):
        raise NotImplementedError

    def retrieve_stored_puzzle(self):
        raise NotImplementedError

    def store_solution(self):
        raise NotImplementedError

    def retrieve_stored_solution(self):
        raise NotImplementedError

    def retrieve_embeddings(self, words : list):
        placeholders = ', '.join(['%s'] * len(words))
        self.cursor.execute(f"""
            select token, vector from embeddings e
            where token in ({placeholders});
        """, words)
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()
        self.cursor.close()
