#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created By Rachit Thariani on 18th Aug, 2021
"""
import sys
import os
from flask import jsonify, request
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from notification_service.notification_handler import PublishNotification
from redis_ratelimit.redis_handler import RedisHandler

class Notification(object):
    def __init__(self):
        self._content = None
        self._channel = None
        self._type = None
        self._id = None

    def user_notification(self, user_id):
         if not user_id:
             response = jsonify({'Message': 'Invalid user Id'})
             return response
         # VALIDATE USER ID
         if request.method == 'POST':
             self._id = user_id
             data = request.form
             if len(request.form) > 0:
                 if 'content' in data:
                    self._content = data['content']
                 else:
                    response = jsonify({'Message': 'Invalid content'})
                    return response
                 if 'channel' in data:
                    self._channel = data['channel']
                 else:
                    response = jsonify({'Message': 'Invalid channel'})
                    return response
                 if 'type' in data:
                    self._type = data['type']
                 else:
                    response = jsonify({'Message': 'Invalid type'})
                    return response

         redis = RedisHandler()
         res = redis.rate_limit(int(self._id))
         if not res:
             response = jsonify({'Message': 'Too many requests. Please wait.'})
             return response
         else:
             response = jsonify({'Message': self._channel + ' sent.'})
             publish_notification = PublishNotification(self._content, self._channel, self._type, self._id)
             publish_notification.populate_kafka()
             return response

    def group_notification(self, group_id):
         if not group_id or not int(group_id):
             response = jsonify({'Message': 'Invalid group Id'})
             return response
         # VALIDATE Group ID
         self._id = group_id
         redis = RedisHandler()
         res = redis.rate_limit(int(self._id))
         if not res:
             response = jsonify({'Message': 'Too many requests. Please wait.'})
             return response
         else:
             count = 0
             if request.method == 'POST':
                 for id in range(int(group_id)):
                     self.user_notification(id)
                     count += 1
             if count == int(group_id):
                response = jsonify({'Message':  'Sent.'})
                return response
             else:
                 response = jsonify({'Message': 'Failed to deliver.'})
                 return response


