from flask import Flask, render_template, redirect, url_for, request, Response
import pymysql
import json
import logging
from datetime import datetime
import os

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

c_info = {
    "host": os.environ['rds_host'],
    "user": os.environ['rds_user'],
    "password": os.environ['rds_password'],
    "cursorclass": pymysql.cursors.DictCursor,
}

user_table_name = "rds_user_service.users"
address_table_name = "rds_user_service.address"
user_fields = ["last_name", "first_name", "email", "hashed_password",
               "status", "created_date"]
address_fields = ["street_no_1", "street_no_2", "city", "state",
                  "country", "postal_code"]


def log_and_extract_input(path_params=None):
    path = request.path
    args = dict(request.args)
    headers = dict(request.headers)
    method = request.method

    try:
        if request.data is not None:
            data = request.json
        else:
            data = None
    except Exception as e:
        # This would fail the request in a more real solution.
        data = "You sent something but I could not get JSON out of it."

    log_message = str(datetime.now()) + ": Method " + method

    inputs = {
        "path": path,
        "method": method,
        "path_params": path_params,
        "query_params": args,
        "headers": headers,
        "body": data
    }

    log_message += " received: \n" + json.dumps(inputs, indent=2)
    logger.debug(log_message)

    return inputs


def create_update_by_id_statement(table_name, parameters, data, id):
    if not parameters:
        return ""
    sql = """UPDATE {} set """.format(table_name)
    for parameter in parameters:
        if parameter in data:
            sql += """{} = "{}", """.format(parameter, data[parameter])
    sql = sql[:-2]
    sql += """ where id = {}""".format(id)
    return sql


def create_select_by_id_statement(table_name, id):
    return """SELECT * FROM {} where id = {}""".format(table_name, id)


def create_delete_by_id_statement(table_name, id):
    return """DELETE FROM {} where id = {}""".format(table_name, id)


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
    sql = create_select_by_id_statement(user_table_name, id)
    conn = pymysql.connect(**c_info)
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            rsp = Response(json.dumps(cursor.fetchall()), status=200, content_type="application/json")
            return rsp
        except (pymysql.Error, pymysql.Warning) as e:
            print(e)
            conn.rollback()
            rsp = Response("Internal Server Error", status=500, content_type="application/json")
            return rsp
        finally:
            conn.close()


@app.route('/Users/<id>', methods=['PUT'])
def update_users_by_id(id):
    inputs = log_and_extract_input()
    data = inputs["body"]
    sql = create_update_by_id_statement(user_table_name, user_fields, data, id)
    if not sql:
        rsp = Response("Nothing to Update", status=200, content_type="application/json")
        return rsp
    conn = pymysql.connect(**c_info)
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            conn.commit()
            rsp = Response("Successful Update", status=200, content_type="application/json")
            return rsp
        except (pymysql.Error, pymysql.Warning) as e:
            print(e)
            rsp = Response("Internal Server Error", status=500, content_type="application/json")
            return rsp
        finally:
            conn.close()


@app.route('/Users/<id>', methods=['DELETE'])
def delete_users_by_id(id):
    sql = create_delete_by_id_statement(user_table_name, id)
    conn = pymysql.connect(**c_info)
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            conn.commit()
            rsp = Response("Successful Delete", status=200, content_type="application/json")
            return rsp
        except (pymysql.Error, pymysql.Warning) as e:
            print(e)
            rsp = Response("Internal Server Error", status=500, content_type="application/json")
            return rsp
        finally:
            conn.close()


@app.route('/Addresses/<id>', methods=['GET'])
def get_addresses_by_id(id):
    sql = create_select_by_id_statement(address_table_name, id)
    conn = pymysql.connect(**c_info)
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            rsp = Response(json.dumps(cursor.fetchall()), status=200, content_type="application/json")
            return rsp
        except (pymysql.Error, pymysql.Warning) as e:
            print(e)
            rsp = Response("Internal Server Error", status=500, content_type="application/json")
            return rsp
        finally:
            conn.close()


@app.route('/Addresses/<id>', methods=['PUT'])
def update_addresses_by_id(id):
    inputs = log_and_extract_input()
    data = inputs["body"]
    sql = create_update_by_id_statement(address_table_name, address_fields, data, id)
    if not sql:
        rsp = Response("Nothing to Update", status=200, content_type="application/json")
        return rsp
    conn = pymysql.connect(**c_info)
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            conn.commit()
            rsp = Response("Successful Update", status=200, content_type="application/json")
            return rsp
        except (pymysql.Error, pymysql.Warning) as e:
            print(e)
            rsp = Response("Internal Server Error", status=500, content_type="application/json")
            return rsp
        finally:
            conn.close()

@app.route('/Addresses/<id>', methods=['DELETE'])
def delete_addresses_by_id(id):
    sql = create_delete_by_id_statement(address_table_name, id)
    conn = pymysql.connect(**c_info)
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql)
            conn.commit()
            rsp = Response("Successful Delete", status=200, content_type="application/json")
            return rsp
        except (pymysql.Error, pymysql.Warning) as e:
            print(e)
            rsp = Response("Internal Server Error", status=500, content_type="application/json")
            return rsp
        finally:
            conn.close()


def main():
    app.run(debug=True, threaded=True, host='0.0.0.0', port='5000')


if __name__ == "__main__":
    main()
