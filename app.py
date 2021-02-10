from flask import Flask, request, render_template, redirect
from connection import connect
from models import User


app = Flask(__name__)


@app.route('/')
def index():
    message = None
    loged_in_check = False
    connection = connect()
    cursor = connection.cursor()
    check_for_login = User.login_check(cursor)
    if check_for_login:
        loged_in_check = True

    return render_template('index.html', loged_in_check = loged_in_check, message = message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    connection = connect()
    cursor = connection.cursor()
    if request.method == 'POST':
        new_user = User(request.form['username'], request.form['first_name'], request.form['last_name'], request.form['password'])
        adding_user = new_user.add_user(cursor)
        if adding_user == 'user_added':
            message = 'User added to data base'
    connection.close()

    return render_template('register.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    connection = connect()
    cursor = connection.cursor()
    if request.method == 'POST':
        login_check = User.log_in(request.form['username'], request.form['password'], cursor)
        if login_check == 'no user':
            message = 'Wrong username bitch!'
        elif login_check == 'wrong password':
            message = 'Wrong password bitch!'
        elif login_check == 'loged in':
            message = 'You have logged in'
            return redirect('/')
    connection.close()

    return render_template('login.html', message = message)


@app.route('/users')
def user():
    return render_template('users.html')


if __name__ == '__main__':
    app.run()
