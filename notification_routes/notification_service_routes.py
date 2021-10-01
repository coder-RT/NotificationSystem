import os
import sys
from flask import Blueprint
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from notification_service.notification import Notification

notification = Notification()
notification_bp = Blueprint('notification_bp', __name__)
notification_bp.route('/notification/user/<user_id>', methods=['POST'])(notification.user_notification)
notification_bp.route('/notification/group/<group_id>', methods=['POST'])(notification.group_notification)
