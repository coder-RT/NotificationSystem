from provider_interface import ProviderInterface
import os
import sys
import ast
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from redis_ratelimit.redis_handler import RedisHandler
from notification_commons.config import PUSH_NOTIFICATION_TOPIC, PUSH_TIMEOUT_MS
from kafka_service.kafka_consumer import Consumer

class PushMessage(ProviderInterface):
    def __init__(self):
        super(ProviderInterface, self).__init__()

    def calculate_priority(self):
        pass

    def send_notification(self):
        consumer_obj = Consumer()
        consumer_obj.set_consumer(PUSH_NOTIFICATION_TOPIC)
        consumer = consumer_obj.get_consumer()

        redis = RedisHandler()
        while True:
            msg_pack = consumer.poll(timeout_ms=PUSH_TIMEOUT_MS)
            for tp, message in msg_pack.items():
                data = ast.literal_eval(message[0].value.decode('utf-8'))
                res = redis.rate_limit(int(data['id']))
                if res:
                    content = data["content"]
                    sys.stdout.write("Push sent: " + str(content))
                else:
                    sys.stdout.write("Too many requests. Please Wait.")

if __name__ == '__main__':
    pm = PushMessage()
    pm.send_notification()