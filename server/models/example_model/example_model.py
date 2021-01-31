# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Column, Integer, Float, JSON, DATE, Text, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid
from server.dbs.db import engine_psql, session_psql, session_mysql, engine_mysql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
# 创建基础的元数据
base_one = declarative_base()


class Name(base_one):
    __tablename__ = 'name'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    mail = Column(Text, nullable=False, index=True)
    phone = Column(Text)
    name = Column(Text)
    password = Column(String(256), nullable=False)
    avatar = Column(Text)
    sex = Column(Text)
    signtime = Column(DATE, default=datetime.datetime.now)


class User(base_one):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, unique=True, nullable=False, index=True)
    # user_id = Column(Text, unique=True, nullable=False, index=True, default=uuid.uuid4().hex)
    mail = Column(Text, nullable=False, index=True)
    phone = Column(Text)
    name = Column(Text)
    _password_hash_ = Column(String(256), nullable=False)
    avatar = Column(Text)
    sex = Column(Text)
    signtime = Column(DATE, default=datetime.datetime.now)

    # 设置访问密码的方法,并用装饰器@property设置为属性,调用时不用加括号
    @property
    def password(self):
        raise Exception('password can not be read')

    # 设置加密的方法,传入密码,对类属性进行操作
    @password.setter
    def password(self, value):
        self._password_hash_ = generate_password_hash(value)

    # 设置验证密码的方法
    def check_password(self, user_pwd):
        return check_password_hash(self._password_hash_, user_pwd)


if __name__ == '__main__':
    pass
    # base_one.metadata.drop_all(engine_psql)
    # base_one.metadata.create_all(bind=engine_psql)
    # base_one.metadata.create_all(bind=engine_mysql)

    # 插入一百万条数据
    # import uuid
    # with session_psql() as sess:
    #     for i in range(10):
    #         print(i)
    #         user_id = uuid.uuid4()
    #         mail = user_id.hex + str(i) + '@qq.com'
    #         phone = str(i)
    #         password = str(i)
    #         obj = Name(
    #             uuid=user_id,
    #             mail=mail,
    #             phone=phone,
    #             password=password
    #             )
    #         sess.add(obj)








