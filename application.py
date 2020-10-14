from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

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





