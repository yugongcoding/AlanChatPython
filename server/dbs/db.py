# -*- coding: utf-8 -*-
import redis
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from functools import partial
from contextlib import contextmanager
from server.config.setting import db_url
import logging


@contextmanager
def create_session(db_session):
    """
    创建一个会话生成器  不占用内存且具有上下文作用
    :param db_session: 一个虚拟的数据库会话对象
    :return: None Return
    """
    sess = db_session()
    try:
        # yield以上的代码是在上下文进入的时候执行  离开时执行下面的代码
        yield sess
        sess.commit()
    except Exception as e:
        # 出错的话则回滚
        logging.debug(str(e))
        sess.rollback()
    else:
        # 没出错则关闭会话连接
        sess.close()


# 创建物理连接  创建成功则输出
engine_psql = create_engine(db_url['data_base_postgresql'], echo=False)
engine_mysql = create_engine(db_url['data_base_mysql'], echo=False)

# 创建虚拟连接  可以创建多个数据库连接对象
Session_one = sessionmaker(bind=engine_psql)
Session_mysql = sessionmaker(bind=engine_mysql)

# 创建持久会话  可以创建多个数据库持久化连接会话
# partial的作用相当于把一个上下文函数编程一个类，这样我们可以通过with语句来操作上下文
# 使用方法是
# with session_zs() as session:
#         print(session_zs)
#         print(session)
#         session.query()
# partial就像把一个函数变成一个类
session_psql = partial(create_session, db_session=Session_one)
session_mysql = partial(create_session, db_session=Session_mysql)

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
redis_session = redis.Redis(host='localhost', port=6379, decode_responses=True, connection_pool=pool)
redis_session.set('name', 'runoob')  # 设置 name 对应的值


if __name__ == '__main__':
    print(type(session_psql))

