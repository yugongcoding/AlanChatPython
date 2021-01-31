# 导入需要的包文件
import threading
import uuid
from flask import Blueprint, g, request, make_response
from flask_mail import Mail, Message
from flask_restx import Api, Resource
from server.api.api_server import api_server
from threading import Thread
import time

from server.config.config import Config

mail_blueprint = Blueprint('mail_blueprint', __name__)

mail_api = Api(mail_blueprint)


@mail_blueprint.after_request
def af_req(resp):  #解决跨域session丢失
    print('ejwiujwei')
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Origin'] = Config.accessControlAllowOrigin

    resp.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE,OPTIONS'
    #resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild'
    resp.headers['X-Powered-By'] = '3.2.1'
    resp.headers['Content-Type'] = 'application/json;charset=utf-8'
    return resp


@mail_blueprint.before_request
def create_mail():
    g.mail = Mail(api_server)
    # with api_server.app_context():
    #     g.mail = Mail(api_server)


def run():
    time.sleep(4)
    print('当前线程的名字是： ', threading.current_thread().name)
    time.sleep(2)


@mail_api.route('/getMailCode')
class MailSend(Resource):
    @staticmethod
    def post():
        mailCode = str(uuid.uuid1())[:6]
        mail = request.json['mail']
        print(mail)
        thr1 = Thread(target=MailSend.send_mail, args=(g.mail, mail, mailCode,))
        thr1.start()
        return mailCode

    @staticmethod
    def send_mail(mail, user_mail, mail_code):
        with api_server.app_context():
            message = Message(subject='AlanChat邮箱安全验证码！', recipients=[user_mail, ],
                              body='您的邮箱安全验证码为{}，有效期为五分钟，请及时进行登录验证！'.format(mail_code))
            mail.send(message=message)


@mail_api.route('/send_mail')
class Wss(Resource):
    # 接收get请求 在flask视图函数中  设置守护线程是无效的存在  所有的线程只能是非守护线程
    @staticmethod
    def get():
        # start_time = time.time()
        #
        # print('这是主线程：', threading.current_thread().name)
        # thread_list = []
        # for i in range(5):
        #     t = threading.Thread(target=run)
        #     thread_list.append(t)
        #
        # for t in thread_list:
        #     t.setDaemon(True)
        #     t.start()
        #
        # print('主线程结束了！', threading.current_thread().name)
        # print('一共用时：', time.time() - start_time)
        # 新开启的线程并不知道有上下文变量的存在 就如同新来的员工 并不知道有g.mail的存在，所以要告诉它这个全局变量的存在
        # Wss.send_mail(mail=g.mail)
        thr1 = Thread(target=Wss.send_mail, args=(g.mail, ))
        thr1.start()
        # thr2 = Thread(target=Wss.send_mail, args=(g.mail,))
        # thr1 = Thread(target=run,)
        # thr2 = Thread(target=run,)
        # thr1.setDaemon(True)
        # thr2.setDaemon(True)

        # thr2.start()
        # thr1.join()
        # thr2.join()
        # print('=========================')
        # thr.join()
        # Wss.send_mail()
        # message = Message(subject='hello world!', recipients=['3302362169@qq.com', 'zs13128488417@gmail.com'],
        #                   body='我只是简单测试一下自动sdhjw蓝图发送邮箱服务！')
        # g.mail.send(message=message)
        return 'mail send successfully!'

    @staticmethod
    def send_mail(mail):
        # mail = Mail(api_server)
        # mail.init_app(api_server)
        with api_server.app_context():
            message = Message(subject='hello world!', recipients=['3302362169@qq.com', 'zs13128488417@gmail.com'],
                              body='我只是简单测试一下自动sdhjw蓝图发送邮箱服务！')
            mail.send(message=message)
