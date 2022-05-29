from database.mongodb import mongodb
from kafka import KafkaConsumer
from json import loads


class consumer_problem:
    def __init__(self):
        self.database = mongodb()
        self.consumer = KafkaConsumer(
            'problemInfo',
            bootstrap_servers=['localhost:9092'],
            auto_offset_rest='earliest',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            consumer_timeout_ms=1000
        )

    def saveData(self):
        for message in self.consumer:
            self.database.insertProblemDocument(message)


class consumer_user:
    def __init__(self):
        self.database = mongodb()
        self.consumer = KafkaConsumer(
            'userInfo',
            bootstrap_servers=['localhost:9092'],
            auto_offset_rest='earliest',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            consumer_timeout_ms=1000
        )

    def saveData(self):
        for message in self.consumer:
            self.database.insertUserDocument(message)