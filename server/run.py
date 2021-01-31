# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.api.api_server import api_server
from loguru import logger
from server.api.application_socket_one.flask_socket import socketio
from flask_cors import *

from datetime import timedelta
from server.api.application_one.app_one_views import app_one_api
from server.api.application_one.mail_views import mail_blueprint

logger.info('test！')

api_server.register_blueprint(app_one_api, url_prefix='/alan-api')
api_server.register_blueprint(mail_blueprint, url_prefix='/alan-api')

CORS(api_server, supports_credentials=True)
CORS(api_server, resources=r'/*')
socketio.init_app(api_server, cors_allowed_origins='*', async_mode='eventlet')

if __name__ == '__main__':
    # api_server.run(host='127.0.0.1', port=5000, debug=True)  192.168.1.102
    socketio.run(api_server, host='127.0.0.1', port=5000, debug=True)
