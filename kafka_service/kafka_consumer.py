import os
import sys
from kafka import KafkaConsumer
from json import loads
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from notification_commons.config import KAFKA_BOOTSTRAP_SERVER, AUTO_OFFSET_RESET, ENABLE_AUTO_COMMIT, GROUP_ID

class Consumer():
    def __init__(self):
        self.topic = None
        self.consumer = None
    def set_consumer(self, topic):
        self.topic = topic
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
            auto_offset_reset=AUTO_OFFSET_RESET,
            enable_auto_commit=ENABLE_AUTO_COMMIT,
            group_id=GROUP_ID,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
    def get_consumer(self):
        return self.consumer
