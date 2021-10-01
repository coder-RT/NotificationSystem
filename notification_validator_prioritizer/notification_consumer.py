import sys
import os
import ast
from kafka import KafkaConsumer
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from notification_service.push_handler import PublishPush
from notification_service.sms_handler import PublishSms

def validator():

    consumer = KafkaConsumer('notifications',
                             group_id='my-group',
                             bootstrap_servers=['localhost:9092'])
    while True:
        msg_pack = consumer.poll(timeout_ms=500)
        for tp, message in msg_pack.items():

            data = ast.literal_eval(message[0].value.decode('utf-8'))
            channel = data["channel"]
            if channel.lower() == "push":
                # publish to priority 1
                print("channel is push.")
                publish_push = PublishPush()
                publish_push.publish_to_push(data)
            if channel.lower() == "sms":
                # publish to priority 2
                print("channel is sms")
                publish_push = PublishSms()
                publish_push.publish_to_sms(data)


if __name__ == '__main__':
    validator()


