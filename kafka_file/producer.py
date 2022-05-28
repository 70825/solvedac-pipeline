from kafka import KafkaProducer
from json import dumps


class producer:
    def __init__(self):
        self.producer = KafkaProducer(
            acks=0,
            compression_type='gzip',
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )

    def send(self, topic_name, value):
        self.producer.send(topic=topic_name, value=value)
        self.producer.flush()
