from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__) # 플라스크 임포트

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.hh99_nickname # db연결

import jwt
import datetime
import hashlib

SECRET_KEY = 'TEAM19'

# html 연결하기
@app.route('/')
def home():
    return render_template('Login.html') # 메인 페이지(로그인)

@app.route('/ChooseMyname')
def get_name():
    return render_template('ChooseMyname.html') # 닉네임 생성 페이지

@app.route('/myPage')
def get_myname():
    return render_template('myPage.html') # 마이 페이지

# html 연결하기 끝

@app.route('/') # 로그인 완료 / 토큰 확인
def sign_ok():
    token_receive = request.cookies.get('mytoken')
    request.args.get(token_receive)
    try:
        return render_template('Login.html', token_receive=request.cookies.get('mytoken'))
    except jwt.ExpiredSignatureError:
        return redirect(url_for(sign_ok, msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for(sign_ok, msg="로그인 정보가 존재하지 않습니다."))

@app.route('/get_mynick', methods=['GET'])
def get_mynick():
    # nickname = list(db.hh99_nickname.find({'class':'adj'}, {'_id': False})) # 윤재님 DB
    nickname = list(db.wordsdb.find({}, {'_id': False}))    # 우석 개인 DB
    return jsonify({'all_nickname': nickname})

@app.route('/api/sign_up', methods=['POST']) # 회원가입 기능
def api_sign_up():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw2_receive = request.form['pw2_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {'id': id_receive,
           'pw': pw_hash}

    db.usersdb.insert_one(doc)

    return jsonify({'msg': '회원가입 완료!'})

# 기능 구현(로그인)
@app.route('/api/sign_in', methods=['POST'])
def api_sign_in():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    user_info = db.usersdb.find_one({'id': id_receive, 'pw': pw_hash})

    if user_info is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token, 'data': user_info['id']}) # 토큰 부여

        return render_template('ChooseMyname.html', token)
    else:
        return jsonify({'result': 'fail', 'msg': '아이디나 패스워드를 확인하세요'}) # 유저정보없으면 토큰X

# 기능 구현 (토큰 확인)
@app.route('/api/sign_ok', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.usersdb.find_one({'id': payload['id']}, {'_id': 0})

        return jsonify({'result': 'success', 'userid': userinfo['id']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 없습니다.'})

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
@app.route('/order', methods=['GET'])
def view_nick():
    nick = list(db.mynick.find({},{'_id':False}))
    return jsonify({'nick':nick})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


