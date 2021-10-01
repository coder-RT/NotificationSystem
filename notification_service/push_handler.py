import sys
import os
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from notification_service.notification_handler import PublishNotification
from notification_commons.config import PUSH_NOTIFICATION_TOPIC, PUSH_NOTIFICATION_KEY

class PublishPush(PublishNotification):
    def __init__(self):
        pass

    def publish_to_push(self, data):
        kafka_connect_publish = super().get_kafka_connection()
        producer = super().get_kafka_producer()
        kafka_connect_publish.publish_message(producer, PUSH_NOTIFICATION_TOPIC, PUSH_NOTIFICATION_KEY, data)

