from flask import Flask, render_template, jsonify, request
app = Flask(__name__) # 플라스크 임포트

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.hh99 # 파이몽고 임포트

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


