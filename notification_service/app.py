import sys
import os
from flask import Flask
from flask_cors import CORS
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from notification_commons.config import DEBUG
from notification_routes.notification_service_routes import notification_bp

app = Flask(__name__)

CORS(app)
resources = {r"/api/*": {"origins": "*"}}
app.config["CORS_HEADERS"] = "Content-Type"
app.config['JSON_SORT_KEYS'] = False

app.register_blueprint(notification_bp)

if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host='0.0.0.0')