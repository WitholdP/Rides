class User(object):
    """class for creating Users in the database"""

    def __init__(self, username = "", first_name = "", last_name = "", password = ""):
        self._id = -1
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self._password = password


    @property
    def id(self):
        return self._id


    def add_user(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users (username, first_name, last_name, password) VALUES (%s, %s, %s, %s)"""
            values = (self.username, self.first_name, self.last_name, self._password)
            cursor.execute(sql, values)
            return 'user_added'
        return False


    @staticmethod
    def log_in(username, password, cursor):
        """Login function:
            1 - it checkes if username exists in data database
            2 - if password matches username it sets value of loged_in parameter to True, for this user"""

        sql = f"""SELECT * FROM users WHERE username = '{username}' ;"""
        cursor.execute(sql)
        check_if_exists = cursor.fetchone()
        if check_if_exists:
            if password == check_if_exists[4]:
                log_in_sql = f"""UPDATE users SET loged_in = True WHERE username = '{username}';"""
                cursor.execute(log_in_sql)
                return 'loged in'
            else:
                return 'wrong password'
        else:
            return 'no user'


    @staticmethod
    def login_check(cursor):
        """ Function will check if any of the users has atribute loged_in set to True.
        If yes it will change teh contect on the page. Some pages will not be available
        for users that are not logged in."""

        sql = """SELECT * FROM users WHERE loged_in = True ;"""
        cursor.execute(sql)
        check = cursor.fetchone()
        if check:
            return check


    @staticmethod
    def logout(cursor):
        sql = """UPDATE users SET loged_in = False WHERE loged_in = True"""
        cursor.execute(sql)
        return True


    @staticmethod
    def update_user(cursor, username, first_name, last_name, password):
        """Gets all the data from edit form (regardless of change) and updates it in the database"""
        sql = f"""UPDATE users SET first_name = '{first_name}', last_name = '{last_name}', password = '{password}' WHERE username = '{username}'"""
        cursor.execute(sql)
        return True


    @staticmethod
    def delete_account(cursor, id, password):
        sql = f"""SELECT * FROM users WHERE id = '{id}' ;"""
        cursor.execute(sql)
        fetch_user = cursor.fetchone()
        if fetch_user:
            if password == fetch_user[4]:
                delete_sql = f"""DELETE FROM users WHERE id = '{id}' ;"""
                cursor.execute(delete_sql)
                return True
            else:
                return False


    @staticmethod
    def get_all_users(cursor):
        sql = """SELECT * FROM users"""
        users_list = []
        cursor.execute(sql)
        users = cursor.fetchall()
        for user in users:
            users_list.append(user)
        return users_list

class Message():
    """Class created for the mesages in the database"""

    def __init__(self, from_id, to_id, message=""):
        self.from_id = from_id
        self.to_id = to_id
        self.message = message

    def send_message(self, cursor):
        sql = """INSERT INTO messages (from_id, to_id, message) Values (%s, %s, %s)"""
        values = (self.from_id, self.to_id, self.message)
        cursor.execute(sql, values)
        return True

    @staticmethod
    def inbox(cursor, user_id):
        """ SQL joins the sender of the message and for filtering is user the id of loged in user"""

        sql = f"""SELECT username, message, creation_date FROM messages LEFT JOIN users ON messages.from_id = users.id WHERE to_id = '{user_id}';"""
        messages = []
        cursor.execute(sql)
        get_messages = cursor.fetchall()
        for message in get_messages:
            messages.append(message)
        return messages


    @staticmethod
    def sent(cursor, user_id):
        """reversed sql to the inbox"""
        sql = f"""SELECT username, message, creation_date FROM messages LEFT JOIN users ON messages.to_id = users.id WHERE from_id = '{user_id}';"""
        messages = []
        cursor.execute(sql)
        get_messages = cursor.fetchall()
        for message in get_messages:
            messages.append(message)
        return messages
