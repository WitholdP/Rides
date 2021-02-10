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


    def __str__(self):
        return self.username
