# -*- coding: utf-8 -*-
import datetime

import redis
from flask import Blueprint, request, session, make_response, current_app, redirect, url_for
from threading import Thread

from flask_mail import Mail, Message
from flask_restx import Api, Resource
from server.api.api_server import api_server
from server.config.config import Config
from server.dbs.db import engine_psql, session_psql, session_mysql, engine_mysql, redis_session
from server.models.example_model.example_model import User
import uuid
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app_one_api = Blueprint('app_one_api', __name__)

api_one = Api(app_one_api)


def verify_token(token):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 转换为字典
        data = s.loads(token)
        return True
    except Exception as ex:
        print(ex)
        return False


def create_token(user_id):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600*24*180)
    # 接收用户id转换与编码
    token = s.dumps({"id": user_id}).decode("ascii")
    return token


@api_one.route('/register')
class Register(Resource):
    # 接收get请求
    @staticmethod
    def post():
        mail = request.json['mail']
        password = request.json['password']

        # if 'logined' not in session:
        with session_psql() as sess:
            query = sess.query(User).filter(User.mail == mail).first()
            if query is None:
                thred = Thread(target=Register.userRegisterRemind, args=())
                thred.start()
                userid = uuid.uuid4().hex
                session['userid'] = userid
                session['token'] = create_token(user_id=userid)
                session.permanent = datetime.timedelta(days=180)
                obj = User(
                    mail=mail,
                    password=password,
                    uuid=userid
                )
                sess.add(obj)
                return True
            else:
                return False

    @staticmethod
    def userRegisterRemind():
        mail = Mail(api_server)
        with api_server.app_context():
            message = Message(subject='AlanChat新用户注册提醒！', recipients=[api_server.config.get('MAIL_USERNAME'), ],
                              body='有新用户注册啦！')
            mail.send(message=message)


@api_one.route('/login')
class Login(Resource):
    # 接收get请求
    @staticmethod
    def post():
        mail = request.json['mail']
        password = request.json['password']
        with session_psql() as sess:
            query = sess.query(User).filter(User.mail == mail).first()
            if query is None or not query.check_password(password):
                return False
            else:
                session['userid'] = query.uuid
                session['token'] = create_token(user_id=query.uuid)
                session.permanent = datetime.timedelta(days=180)
                return [True, query.name, query.avatar, query.uuid]


@api_one.route('/getUserInfo')
class GetUserInfo(Resource):
    # 接收get请求
    @staticmethod
    def get():
        userid = session['userid']
        with session_psql() as sess:
            query = sess.query(User.name, User.avatar, User.uuid).filter(User.uuid == userid).first()
        return [query[0], query[1], query[2]]


@api_one.route('/initChatList')
class InitChatList(Resource):
    # 接收get请求
    @staticmethod
    def get():
        userid = session['userid']
        all_user = []
        with session_psql() as sess:
            query = sess.query(User).all()
            for i in range(len(query)):
                data = query[i]
                info = {
                        'id': i + 1,
                        'user': {
                            'name': data.name,
                            'img': data.avatar,
                            'user_id': data.uuid
                        },
                        'messages': [
                            {
                                'content': '你好，我们已经是新朋友了',
                                'date': str(datetime.datetime.now())
                            }
                        ],
                        'index': i + 1
                    }
                all_user.append(info)
        return all_user


@api_one.route('/judgeLoginStatus')
class Wss(Resource):
    # 接收get请求
    @staticmethod
    def get():
        res = verify_token(session.get('token'))
        return res


@api_one.route('/getSession')
class Wss(Resource):
    # 接收get请求
    @staticmethod
    def get():
        return 'hello world'


@app_one_api.after_request
def af_req(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Origin'] = Config.accessControlAllowOrigin
    resp.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE,OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Length, Authorization, Accept, ' \
                                                   'X-Requested-With , yourHeaderFeild '
    resp.headers['X-Powered-By'] = '3.2.1'
    resp.headers['Content-Type'] = 'application/json;charset=utf-8'
    return resp


@api_one.route('/test_redis')
class Redis(Resource):
    # 接收get请求
    @staticmethod
    def get():
        return redis_session.get('name')
