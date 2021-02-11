from flask import Flask, request, render_template, redirect
from connection import connect
from models import User, Message


app = Flask(__name__)


@app.route('/')
def index():
    connection = connect()
    cursor = connection.cursor()
    check_for_login = User.login_check(cursor)
    connection.close()
    return render_template('index.html', check_for_login = check_for_login)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    connection = connect()
    cursor = connection.cursor()
    check_for_login = User.login_check(cursor)
    if check_for_login:
        return redirect('/')
    if request.method == 'POST':
        new_user = User(request.form['username'], request.form['first_name'], request.form['last_name'], request.form['password'])
        adding_user = new_user.add_user(cursor)
        if adding_user == 'user_added':
            message = 'User added to data base'

    connection.close()
    return render_template('register.html', message=message, check_for_login = check_for_login)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    connection = connect()
    cursor = connection.cursor()
    check_for_login = User.login_check(cursor)
    if check_for_login:
        return redirect('/')
    if request.method == 'POST':
        login_check = User.log_in(request.form['username'], request.form['password'], cursor)
        if login_check == 'no user':
            message = 'Wrong username bitch!'
        elif login_check == 'wrong password':
            message = 'Wrong password bitch!'
        elif login_check == 'loged in':
            connection.close()
            return redirect('/')

    connection.close()
    return render_template('login.html', message = message, check_for_login = check_for_login)


@app.route('/users', methods=['GET', 'POST'])
def users():
    connection = connect()
    cursor = connection.cursor()
    check_for_login = User.login_check(cursor)
    if check_for_login:
        users = User.get_all_users(cursor)
        connection.close()
        return render_template('users.html', check_for_login = check_for_login, users = users)

    connection.close()
    return redirect('/')


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    message = None
    connection = connect()
    cursor = connection.cursor()
    check_for_login = User.login_check(cursor)
    if check_for_login:
        inbox = Message.inbox(cursor, check_for_login[0])
        sent = Message.sent(cursor, check_for_login[0])
        users = User.get_all_users(cursor)
        if request.method == 'POST':
            new_message = Message(check_for_login[0], request.form['to_id'], request.form['message'])
            send_message = new_message.send_message(cursor)
            if send_message:
                message = f"Message sent!"
        connection.close()
        return render_template('messages.html', check_for_login = check_for_login, users = users, message = message, inbox = inbox, sent=sent)

    connection.close()
    return redirect('/')


@app.route('/rides', methods=['GET', 'POST'])
def rides():
    connection = connect()
    cursor = connection.cursor()
    check_for_login = User.login_check(cursor)
    if check_for_login:
        connection.close()
        return render_template('rides.html', check_for_login = check_for_login)

    connection.close()
    return redirect('/')

@app.route('/logout')
def logout():
    connection = connect()
    cursor = connection.cursor()
    logging_out = User.logout(cursor)
    if logging_out:
        connection.close()
        return redirect('/')

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    message = None
    connection = connect()
    cursor = connection.cursor()
    check_for_login = User.login_check(cursor)
    if check_for_login:
        if request.method == 'POST':
            update_user = User.update_user(cursor, **request.form)
            if update_user:
                message = "Succesfully updated user data"
        connection.close()
        return render_template('edit.html', check_for_login = check_for_login, message = message)

    connection.close()
    return redirect('/')


@app.route('/delete/<int:id>/', methods = ['GET', 'POST'])
def delete(id):
    message = None
    connection = connect()
    cursor = connection.cursor()
    check_for_login = User.login_check(cursor)
    if check_for_login:
        if request.method == 'POST':
            delete_account = User.delete_account(cursor, id, request.form['password'])
            if delete_account:
                connection.close()
                return redirect('/')
            else:
                message = 'Wrong password bitch!'
        connection.close()
        return render_template('delete.html', check_for_login = check_for_login, message = message)


if __name__ == '__main__':
    app.run(debug = True)
