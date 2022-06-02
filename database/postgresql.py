import psycopg2


class postgresql:
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

    def findMaxIndex(self, flags):
        '''
        :param flags: True -> problem, False -> user
        :return:
        '''
        target = 'problemid' if flags else 'userid'
        query = f'select max(index) from {target}'
        self.cursor.execute(query)
        count = self.cursor.fetchall()[0][0]

        if count == None: count = 1
        else: count += 1

        return count

