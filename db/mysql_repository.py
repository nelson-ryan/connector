from db.repository import Repository
import mysql.connector
import numpy as np


class MysqlRepository(Repository):

    def __init__(self):
        # super().__init__()
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

    def retrieve_stored_puzzle(self, print_date):
        print(print_date)
        raise NotImplementedError
        self.cursor.execute("""
        """)

    def store_solution(self):
        raise NotImplementedError

    def retrieve_stored_solution(self):
        raise NotImplementedError

    def retrieve_embeddings(self, words : list) -> dict:
        words = [
            str(word) if not isinstance(word, str) else word
            for word in words
        ]
        placeholders = ', '.join(['%s'] * len(words))
        self.cursor.execute(f"""
            select token, vector from embeddings e
            where token in ({placeholders});
        """, words)
        d = {tok : np.array(vec.split())
             for tok, vec in self.cursor.fetchall()}
        return d

    def __del__(self):
        self.cursor.close()
        self.connection.close()
