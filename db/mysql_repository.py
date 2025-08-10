from db.repository import Repository
import mysql.connector
import numpy as np
from collections import defaultdict


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


    def store_puzzle(self, nyjson : dict):
        sql = f"""
        set @print_date = %s

        """
        raise NotImplementedError

    def retrieve_stored_puzzle(self, print_date):
        """
        Retrieves and re-recreates json from data in database.
        TODO: Convert to json from a single query
        """
        # First get genral puzzle data to start the dict
        self.cursor.execute("""
            select id, status, editor, print_date
            from puzzles where print_date = %s
        ;""", [print_date])
        pcols = self.cursor.column_names
        pdata = self.cursor.fetchall()[0]
        if not pdata:
            return None

        build_json = {c:v for c, v in zip(pcols, pdata)}
        build_json['print_date'] = print_date
        build_json['categories'] = defaultdict(list)

        # Now fill in categories and cards
        self.cursor.execute("""
            select cat.title, c.content, c.position
            from cards c
            join categories cat on cat.id = c.category_id
            join puzzles p on p.id = cat.puzzle_id
            and p.print_date = %s
        ;""", [print_date])

        cdata = self.cursor.fetchall()
        for card in cdata:
            build_json['categories'][card[0]].append(
                { 'content' : card[1], 'position' : card[2] }
            )
        return build_json

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
