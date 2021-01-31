# -*- coding: utf-8 -*-
from flask_socketio import SocketIO, join_room, send, emit, rooms
from flask import session, request

from server.dbs.db import redis_session

socketio = SocketIO()

user_id_rooms = {}
user_nums = 0


@socketio.on('connect')
def handle_message():
    if session:
        print('sessin', session)
        sid = request.sid
        user_id = session.get('userid')
        redis_session.set(user_id, sid)


@socketio.on('set_room')
def handle_message(message):
    print('---message----', message)
    # global user_nums
    sid = request.sid
    user_id = message
    # user_id_rooms['userid'] = user_id
    redis_session.set(user_id, sid)
    # join_room(room=user_id, sid=sid)
    # session['room'] = 'alan'
    # user_nums += 1


@socketio.on('message')
def handle_message(data):
    receiver_user_id = data['receiver_user_id']
    sender_user_id = data['sender_user_id']
    mess = {
        'message': data['message'],
        'sender_user_id': sender_user_id,
        'receiver_user_id': receiver_user_id
    }
    sid = redis_session.get(receiver_user_id)
    # join_room(sid, request.sid)
    send(message=mess, include_self=False, room=sid)
    # emit(event='receive', room=session['room'])

