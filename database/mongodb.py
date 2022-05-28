import pymongo

class mongodb():
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.database = self.client['solvedac_user']
        self.user = self.database['user']
        self.problem = self.database['problem']

    def insertUserDocument(self, data):
        self.user.insert_one(data)

    def insertProblemDocument(self, data):
        self.problem.insert_one(data)

    def findUserDocument(self, data):
        return self.user.find(data)

    def findProblemDocument(self, data):
        return self.problem.find(data)