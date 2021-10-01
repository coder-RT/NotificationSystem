import sys
from json import dumps
from kafka import KafkaProducer

class KafkaConnectPublish(object):
    def __init__(self):
        pass

    def publish_message(self, producer_instance, topic_name, key, value):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(str(value), encoding='utf-8')
            producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
            producer_instance.flush()
            sys.stdout.write('Message published successfully.')
        except Exception as ex:
            sys.stderr.write('Exception in publishing message')
            sys.stderr.write(str(ex))

    def connect_kafka_producer(self):
        _producer = None
        try:
            _producer = KafkaProducer(
                bootstrap_servers=['localhost:9091'],
                value_serializer=lambda x: dumps(x).encode('utf-8')
            )
        except Exception as ex:
            sys.stderr.write('Exception while connecting Kafka')
            sys.stderr.write(str(ex))
        finally:
            return _producer

if __name__ == '__main__':
    kp = KafkaConnectPublish()
    kp.connect_kafka_producer()
    print(kp)
