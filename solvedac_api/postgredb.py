import psycopg2

class solvedac_DB():
    def __init__(self):
        self.database = psycopg2.connect(host='localhost',
                                         dbname='solvedac',
                                         user='postgres',
                                         password='asdf1234',
                                         port=5432)
        self.cursor = self.database.cursor()

    def __del__(self):
        self.database.close()
        self.cursor.close()

    def readQuery(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        return row

    def insertQuery(self, query):
        self.cursor.execute(query)
        self.database.commit()