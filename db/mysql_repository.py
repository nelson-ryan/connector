import mysql.connector


class MysqlRepository:

    def __init__(self):
        config = {
            'user': 'root',
            'password': 'woof',
            'host': 'mysql',  # When you run this on your machine change it to 'localhost'
            'port': '3306',  # When you run this on your machine change it to '32000'
            'database': 'connector'
        }
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

    def add_puzzle(self):
        pass

    def get_puzzle(self):
        pass

    def get_embedding(self):
        pass

    def __del__(self):
        self.connection.close()
