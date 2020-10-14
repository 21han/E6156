from flask import Flask, render_template, redirect, url_for, request, Response
import pymysql
import json
import os

app = Flask(__name__)

c_info = {
    "host": os.environ['rds_host'],
    "user": os.environ['rds_user'],
    "password": os.environ['rds_password'],
    "cursorclass": pymysql.cursors.DictCursor,
}

conn = pymysql.connect(**c_info)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/login')
def login():
    return 'login'


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


@app.route('/login_test/')
def hello(name=None):
    return render_template('login.html')


@app.route('/Users/<id>', methods=['GET'])
def get_users_by_id(id):
    sql = """SELECT * FROM rds_user_service.users where id = {}""".format(id)
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            rsp = Response(json.dumps(cursor.fetchall()), status=200, content_type="application/json")
            return rsp
        except (pymysql.Error, pymysql.Warning) as e:
            print(f'error! {e}')


@app.route('/Addresses/<id>', methods=['GET'])
def get_addresses_by_id(id):
    sql = """SELECT * FROM rds_user_service.address where id = {}""".format(id)
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            rsp = Response(json.dumps(cursor.fetchall()), status=200, content_type="application/json")
            return rsp
        except (pymysql.Error, pymysql.Warning) as e:
            print(f'error! {e}')


def main():
    app.run(debug=True, threaded=True, host='0.0.0.0', port='5000')


if __name__ == "__main__":
    main()
