import sys
import os
import redis
from datetime import timedelta
from redis_ratelimit import time_bucketed
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from notification_commons.config import REDIS_HOST, REDIS_PORT, DB, DECODE_RESPONSES, MAX_REQUESTS, TIME_DELTA

class RedisHandler(object):
    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=DB, decode_responses=DECODE_RESPONSES)

    def rate_limit(self, user_id):
        if time_bucketed.request_is_limited(self.r, user_id, MAX_REQUESTS, timedelta(seconds=TIME_DELTA)):
            sys.stdout.write('🛑 Request is limited')
            return False
        else:
            sys.stdout.write('✅ Request is allowed')
            return True

if __name__ == '__main__':
    r = RedisHandler()
    r.rate_limit(1)

