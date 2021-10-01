import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(currentdir)
from kafka_service.kafka_publisher import KafkaConnectPublish
from notification_commons.config import NOTIFICATION_TOPIC, NOTIFICATION_KEY

class PublishNotification(object):
    def __init__(self, content, channel, type, id):
        self._content = content
        self._channel = channel
        self._type = type
        self._id = id

    def get_kafka_connection(self):
        return KafkaConnectPublish()
    def get_kafka_producer(self):
        return self.get_kafka_connection().connect_kafka_producer()

    def populate_kafka(self):
        if self._type.lower() == 'personalized':
            notification_data = { "content" : self._content, "channel" : self._channel, "type" : self._type, "id" : self._id}
            if len(notification_data) > 0:
                kafka_connection = self.get_kafka_connection()
                kafka_producer = self.get_kafka_producer()
                kafka_connection.publish_message(kafka_producer, NOTIFICATION_TOPIC, NOTIFICATION_KEY, notification_data)
                if kafka_producer is not None:
                    kafka_producer.close()
        if self._type.lower() == 'group':
            notification_data = { "content" : self._content, "channel" : self._channel, "type" : self._type, "id" : self._id}
            if len(notification_data) > 0 and self._channel.tolower() == "sms":
                kafka_producer = self.get_kafka_producer()
                for user_id in notification_data["id"]:
                    kafka_producer.publish_message(kafka_producer, NOTIFICATION_TOPIC, NOTIFICATION_KEY, notification_data)
                if kafka_producer is not None:
                    kafka_producer.close()