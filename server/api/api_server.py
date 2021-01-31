# -*- coding: utf-8 -*-
import os
from datetime import timedelta

from flask import Flask, current_app
# 导入蓝图
from flask_cors import CORS

api_server = Flask(__name__)

# 设置的参数从系统获取会比较安全 如:os.getenv('MAIL_USERNAME')
api_server.config.update(
    MAIL_SERVER='smtp.qq.com',
    MAIL_USERNAME='1710695204@qq.com',
    MAIL_PASSWORD='ymiuplyyzkzibada',
    MAIL_PORT='587',
    MAIL_USE_TLS=True,
    MAIL_DEFAULT_SENDER=('AlanRick', '1710695204@qq.com'))

api_server.config['SECRET_KEY'] = os.urandom(24)
api_server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=360)  # 配置7天有效
CORS(api_server, supports_credentials=True)
CORS(api_server, resources=r'/*')

