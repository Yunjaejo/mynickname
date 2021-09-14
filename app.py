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
    return render_template('index.html') # 메인 페이지

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html') # 회원가입 페이지

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html') # 로그인 페이지

@app.route('/sign_ok')
def sign_ok():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.usersdb.find_one({"id": payload['id']})
        return render_template('sign_ok.html', userid=user_info["id"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("sign_in", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("sign_in", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/get_name')
def get_name():
    return render_template('get_name.html') # 닉네임 생성 페이지

@app.route('/post_myname')
def post_myname():
    return render_template('post_myname.html') # 닉네임 즐겨찾기 추가하기

@app.route('/get_myname')
def get_myname():
    return render_template('get_myname.html') # 마이 페이지

@app.route('/delete_myname')
def delete_myname():
    return render_template('delete_myname.html') # 닉네임 삭제 페이지

# html 연결하기 끝

# 기능 구현(토큰 확인)


# 기능 구현(회원가입)
@app.route('/api/sign_up', methods=['POST'])
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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token, 'data': user_info['id']})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디나 패스워드를 확인하세요'})

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



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


