from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

SECRET_KEY = 'TEAM19'

client = MongoClient('localhost', 27017)
# db = client.hh99_nickname # db연결
db = client.nickname




# html 연결하기
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.usersdb.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인

    username_receive = request.form['username_give']
    password_receive = request.form['password_give']


    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.usersdb.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
            'username': username_receive,
            'password': password_hash
    }

    db.usersdb.insert_one(doc)

    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.usersdb.find_one({"username": username_receive}))
    # print(value_receive, type_receive, exists)
    return jsonify({'result': 'success', 'exists': exists})


# html 연결하기 끝

@app.route('/get_mynick', methods=['GET'])
def get_mynick():
    # nickname = list(db.hh99_nickname.find({'class':'adj'}, {'_id': False})) # 윤재님 DB
    nickname = list(db.wordsdb.find({}, {'_id': False}))    # 우석 개인 DB
    return jsonify({'all_nickname': nickname})

@app.route('/myPage')
def get_myname():
    return render_template('myPage.html') # 마이 페이지

# 닉네임 db에 저장
@app.route('/save_mynick', methods=['POST', 'GET'])
def save_nick():
    nick_receive = request.form['nick_give']
    cookieId_receive = request.form['cookieId_give']

    id_list = list(db.mynick.find({'cookieId': cookieId_receive}, {'_id': False}))

    id_count = len(id_list)

    print(id_count)


    if id_count < 8:
        doc = {
            'cookieId': cookieId_receive,
            'nick': nick_receive
        }
        db.mynick.insert_one(doc)
    else:
        delete_nick = id_list[0]
        db.mynick.delete_one(delete_nick)
        doc = {
            'cookieId': cookieId_receive,
            'nick': nick_receive
        }
        db.mynick.insert_one(doc)

# 마이페이지에 닉네임 보여주기
@app.route('/view_mynick', methods=['GET'])
def view_nick():

    mynicks = list(db.mynick.find({'cookieId': request.cookies.get('id')}, {'_id': False}))

    return jsonify({'mynicks': mynicks})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

