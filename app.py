# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import hashlib

from module.helper import *


app = Flask(__name__)

_ip_ = get_host_ip()
_port_ = '8080'

exception_percent = 0  # 0-100
duration_max = 1000  # ms
duration_min = 50  # ms

msg_ok_default = {
    'code': 100,
    'message': "OK."
}
msg_error_default = {
    'code': 500,
    'message': "The system is busy, please try again later."
}

users = {
    'sample': {
        'password': "a10d74a680a1c5cf5bfe6cbbaec1d2e1",  # by md5_password()
        'token': "",
        'hobbies': [
            {
                'name': 'reading',
                'frequency': "1 book per month"
            },
            {
                'name': 'running',
                'frequency': "10 km per week"
            }
        ]
    }
}


@app.route('/')
@app.route('/sample')
def index():
    return render_template('index.html', base_url="http://{}:{}/".format(_ip_, _port_))


@app.route('/hello')
def hello():
    return make_response({'code': 100, 'msg': 'Hello Parrot Sample.'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    add_timestamp(msg_ok_default)
    add_tag(msg_ok_default)

    if request.method == 'GET':
        username = request.args.get('username', None)
        password = request.args.get('password', None)
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)

    msg_invalid_input = {
        'code': 101,
        'message': "Invalid username or password, please modify and try again."
    }
    msg_user_exists = {
        'code': 102,
        'message': "User already exists in system, please use another username."
    }

    if not username or not password:
        rsp = make_response(msg_invalid_input)
    elif username in users.keys():
        rsp, _ = random_response(msg_user_exists)
    else:
        rsp, flag = random_response()
        if flag:
            users[username] = {
                'password': md5_password(password),
                'token': "",
                'hobbies': []
            }
    return rsp


@app.route('/unregister', methods=['GET', 'POST'])
def unregister():
    add_timestamp(msg_ok_default)
    add_tag(msg_ok_default)

    username, rsp = is_logged_out()
    if rsp:
        return rsp
    rsp, flag = random_response()
    if flag:
        if username in users.keys():
            del users[username]
        rsp.delete_cookie('username')
        rsp.delete_cookie('token')
    return rsp


@app.route('/login', methods=['GET', 'POST'])
def login():
    add_timestamp(msg_ok_default)
    add_tag(msg_ok_default)

    if request.method == 'GET':
        username = request.args.get('username', None)
        password = request.args.get('password', None)
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)

    msg_invalid_input = {
        'code': 201,
        'message': "The username or password is incorrect, please modify and log in again."
    }

    if not username or not password or \
            username not in users.keys() or md5_password(password) != users[username]['password']:
        return make_response(msg_invalid_input)
    rsp, flag = random_response()
    if flag:
        token = generate_token(username)
        rsp.headers['token'] = users[username]['token'] = token
        rsp.set_cookie('username', username)
        rsp.set_cookie('token', token)
    return rsp


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    add_timestamp(msg_ok_default)
    add_tag(msg_ok_default)

    rsp, flag = random_response()
    if flag:
        username = request.cookies.get('username', None)
        if username:
            users[username]['token'] = ""
            rsp.delete_cookie('username')
            rsp.delete_cookie('token')
    return rsp


@app.route('/my', methods=['GET'])
@app.route('/my_hobby', methods=['GET'])
@app.route('/my_hobbies', methods=['GET'])
@app.route('/hobby_list', methods=['GET'])
def hobby_list():
    add_timestamp(msg_ok_default)
    add_tag(msg_ok_default)

    username, rsp = is_logged_out()
    if rsp:
        return rsp

    rsp, _ = random_response(dict(msg_ok_default, **{'hobbies': users[username]['hobbies']}))
    return rsp


@app.route('/hobby_detail', methods=['GET'])
def hobby_detail():
    add_timestamp(msg_ok_default)
    add_tag(msg_ok_default)

    username, rsp = is_logged_out()
    if rsp:
        return rsp

    name = request.args.get('name', None)
    if not name:
        return random_response(
            {'code': 301, 'message': "Invalid input, 'name' argument is required."}
        )[0]
    for hobby in users[username]['hobbies']:
        if name == hobby['name']:
            return random_response(
                dict(msg_ok_default, **{'detail': hobby})
            )[0]
    return random_response(
        {'code': 302, 'message': "Invalid input, the specified hobby name doesn't exist."}
    )[0]


@app.route('/add_hobby', methods=['GET', 'POST'])
@app.route('/hobby_add', methods=['GET', 'POST'])
def hobby_add():
    add_timestamp(msg_ok_default)
    add_tag(msg_ok_default)

    username, rsp = is_logged_out()
    if rsp:
        return rsp

    if request.method == 'GET':
        name = request.args.get('name', None)
        frequency = request.args.get('frequency', None)
    else:
        name = request.form.get('name', None)
        frequency = request.form.get('frequency', None)

    if not name or not frequency:
        return random_response(
            {'code': 311, 'message': "Invalid input, 'name' and 'frequency' arguments are needed."}
        )[0]

    for hobby in users[username]['hobbies']:
        if name == hobby['name']:
            hobby['frequency'] = frequency
            return random_response(
                dict(msg_ok_default, **{'hobbies': users[username]['hobbies']})
            )[0]
    users[username]['hobbies'].append({
        'name': name,
        'frequency': frequency
    })
    return random_response(
        dict(msg_ok_default, **{'hobbies': users[username]['hobbies']})
    )[0]


@app.route('/remove_hobby', methods=['GET', 'POST'])
@app.route('/hobby_remove', methods=['GET', 'POST'])
def hobby_remove():
    add_timestamp(msg_ok_default)
    add_tag(msg_ok_default)

    username, rsp = is_logged_out()
    if rsp:
        return rsp

    if request.method == 'GET':
        name = request.args.get('name')
    else:
        name = request.form.get('name')

    if name:
        for idx, hobby in enumerate(users[username]['hobbies']):
            if name == hobby['name']:
                del users[username]['hobbies'][idx]
                break
    else:
        if len(users[username]['hobbies']):
            del users[username]['hobbies'][0]
    return random_response(
        dict(msg_ok_default, **{'hobbies': users[username]['hobbies']})
    )[0]


@app.route('/suggest_hobby', methods=['GET'])
@app.route('/hobby_suggest', methods=['GET'])
def hobby_suggest():
    add_timestamp(msg_ok_default)
    add_tag(msg_ok_default)

    username, rsp = is_logged_out()
    if rsp:
        return rsp

    _today = request.args.get('today', now())
    if len(users[username]['hobbies']) <= 1:
        sug_msg = {
            'code': 303,
            'message': "You need to add more hobbies firstly."
        }
    else:
        idx = (int(_today[-1]) + random.randint(0, len(users[username]['hobbies'])-1)) % len(users[username]['hobbies'])
        suggest = users[username]['hobbies'][idx]['name']
        sug_msg = {
            'code': 100,
            'message': "The suggested hobby for today is: {}".format(suggest)
        }
    return random_response(sug_msg)[0]


def random_response(ok_msg=msg_ok_default):
    time.sleep(random.randint(duration_min, duration_max)*1.0/1000)
    if int(exception_percent) >= random.randint(1, 100):
        rsp = make_response(msg_error_default)
        rsp._status = "500 Internal Server Error"
        return rsp, False
    else:
        return make_response(ok_msg), True


def generate_token(user):
    hl = hashlib.md5()
    hl.update("{}_{}".format(user, now_timestamp()).encode('utf-8'))
    return hl.hexdigest()


def md5_password(password, key='Sample'):
    hl = hashlib.md5()
    hl.update("{}_{}".format(key, password).encode('utf-8'))
    return hl.hexdigest()


def is_logged_out():
    username = request.cookies.get('username', None)
    c_token = request.cookies.get('token', None)
    r_token = request.headers.get('token', None)
    msg_logged_out = {
        'code': 211,
        'message': "Login token expired, please log in again."
    }
    msg_logged_by_other = {
        'code': 212,
        'message': "Account logged in by others, please log in again."
    }
    # print("{} {} {}".format(username, c_token, r_token))
    if not r_token or r_token == 'null':
        return None, make_response(msg_logged_out)
    elif r_token != users[username]['token']:
        return None, make_response(msg_logged_by_other)
    return username, None


def add_timestamp(msg):
    msg['timestamp'] = now_timestamp()


def add_tag(msg):
    msg['tag'] = get_random_string(32)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=_port_)
