from database.mongodb import mongodb
from kafka import KafkaConsumer
from json import loads


class consumer_problem:
    def __init__(self):
        self.database = mongodb()
        self.consumer = KafkaConsumer(
            'problemInfo',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            consumer_timeout_ms=1000
        )

    def saveData(self):
        for message in self.consumer:
            data = {
                'problemId': message.value['problemId'],
                'title': message.value['titles'],
                'level': message.value['level'],
                'tag': message.value['tag']
            }
            self.database.insertProblemDocument(data)


class consumer_user:
    def __init__(self):
        self.database = mongodb()
        self.consumer = KafkaConsumer(
            'userInfo',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            consumer_timeout_ms=1000
        )

    def saveData(self):
        for message in self.consumer:
            data = {
                'handle': message.value['handle'],
                'tier': message.value['tier'],
                'solvedCount': message.value['solvedCount'],
                'solvedProblems': message.value['solvedProblems']
            }
            self.database.insertUserDocument(data)