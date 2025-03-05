import sqlite3
from flask_bcrypt import generate_password_hash, check_password_hash
import uuid

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg=":memory:"):
        self.database_arg = database_arg

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        out = None
        for string in sql_string.split(";"):
            try:
                out = cur.execute(string)
            except:
                pass
        return out
        conn.close()

    """
    def print_sql_string(inputstring, params=None):
        '''
        Prints out a string as a SQL string parameterized assuming all strings
        '''

        if params is not None:
            if params != []:
               inputstring = inputstring.replace("%s","'%s'")

        print(inputstring % params)
    """

    def dictfetchall(self, cur):
        ''' Returns query results as list of dictionaries.'''
        returnres = cur.fetchall()
        print(returnres)
        if returnres == []:
            return []

        cols = [a[0] for a in cur.description]
        print(cols)
        result = []
        for row in returnres:
            result.append({a:b for a,b in zip(cols, row)})
        # cursor.close()
        print(result)
        return result



    #-----------------------------------------------------------------------------

    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        # Clear the database if needed
        cur.execute("DROP TABLE IF EXISTS Users")
        conn.commit()

        # Create the users table
        cur.execute("""CREATE TABLE Users(
            Id INTEGER Primary Key AUTOINCREMENT,
            username TEXT Unique,
            password TEXT,
            admin INTEGER DEFAULT 0,
            publicKey TEXT,
            signaturePublicKey TEXT,
            session_id TEXT
        )""")

        conn.commit()

        cur.execute("DROP TABLE IF EXISTS Friends")
        conn.commit()

        cur.execute("""Create Table Friends(
            communication_id INTEGER Primary Key AUTOINCREMENT,
            user1_id INTEGER,
            user1_name TEXT,
            user2_id INTEGER,
            user2_name TEXT
        )""")
        conn.commit()

        cur.execute("DROP TABLE IF EXISTS Communication")
        conn.commit()

        cur.execute("""Create Table Communication(
            communication_id INTEGER,
            message TEXT,
            iv TEXT,
            signature TEXT,
            datetime TEXT,
            sender_name TEXT,
            receiver_name TEXT
        )""")
        conn.commit()

        cur.execute("DROP TABLE IF EXISTS Course")
        conn.commit()

        cur.execute("""Create Table Course(
            course_name TEXT Primary Key,
            course_guide TEXT
        )""")
        conn.commit()

        cur.execute("DROP TABLE IF EXISTS Post")
        conn.commit()

        cur.execute("""Create Table Post(
            post_id INTEGER Primary Key AUTOINCREMENT,
            course_name TEXT,
            title TEXT,
            content TEXT
        )""")
        conn.commit()

        cur.execute("DROP TABLE IF EXISTS Comment")
        conn.commit()

        cur.execute("""Create Table Comment(
            post_id INTEGER,
            comment TEXT
        )""")
        conn.commit()

        course_ls = [["INFO2222", "This course provides computer professionals with an integrated treatment of two key topics: human-computer interaction (HCI) and safety. The basic techniques and ideas of HCI will be studied, with a particular focus on safety related examples and case studies. This course aims to train students to understand the profound challenges in establishing a computer system that meets the human-computer interaction and safety needs of people. It will provide the basic skills needed to assess the effectiveness of a system to meet people's needs for its use in the environment, understand common errors in the system, and find ways to avoid them."], ["COMP3308", "Machine Learning Course"]]

        for c in course_ls:
            sql_cmd = '''
                    INSERT INTO Course(course_name, course_guide)
                    VALUES('{course_name}', "{course_guide}")
                '''

            sql_cmd = sql_cmd.format(course_name=c[0], course_guide=c[1])

            cur.execute(sql_cmd)
            conn.commit()

        sql_cmd = '''
                INSERT INTO Post(post_id, course_name, title, content)
                VALUES(1, 'INFO2222', "e2e Encryption", "What is end to end encryption?")
            '''

        cur.execute(sql_cmd)
        conn.commit()

        comment_ls = [["1", "e2e encryption is perform encryption and decryption in clients side."], ["1", "The server will not be able to see the plaintext although they transfer the ciphertext."]]
        for c in comment_ls:
            sql_cmd = '''
                    INSERT INTO Comment(post_id, comment)
                    VALUES('{post_id}', "{comment}")
                '''

            sql_cmd = sql_cmd.format(post_id=c[0], comment=c[1])

            cur.execute(sql_cmd)
            conn.commit()
        """
        cur.execute("DROP TABLE IF EXISTS SeverPassword")
        conn.commit()

        cur.execute('''Create Table SeverPassword(
            change_role_password TEXT
        )''')
        conn.commit()

        change_role_password = generate_password_hash("changeRole", 10).decode('utf8')
        sql_cmd = '''
                INSERT INTO SeverPassword(change_role_password)
                VALUES("{change_role_password}")
            '''
        sql_cmd = sql_cmd.format(change_role_password = change_role_password)
        cur.execute(sql_cmd)
        conn.commit()
        """

        # Add our admin user
        """
        sql_cmd = '''
                INSERT INTO Users(Id, username, password, admin)
                VALUES({Id},'{username}', "{password}", {admin})
            '''

        admin_password = generate_password_hash(admin_password, 10).decode('utf8')
        print(admin_password)
        print(type(admin_password))
        sql_cmd = sql_cmd.format(Id = 1, username="admin", password=admin_password, admin=1)

        cur.execute(sql_cmd)
        conn.commit()
        """

        conn.close()

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------
    def change_role(self, username):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_cmd = '''
                UPDATE Users
                SET admin = 1
                WHERE username = '{username}';
            '''
        sql_cmd = sql_cmd.format(username=username)
        cur.execute(sql_cmd)
        conn.commit()
        conn.close()

    # Add a user to the database
    def add_user(self, username, password, admin=0):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_cmd = """
                Select *
                From Users
            """
        cur.execute(sql_cmd)

        if self.dictfetchall(cur) == []:
            session_id = uuid.uuid4().hex
            sql_cmd = '''
                    INSERT INTO Users(Id, username, password, admin, session_id)
                    VALUES({Id},'{username}', "{password}", {admin}, '{session_id}')
                '''

            password = generate_password_hash(password, 10).decode('utf8')
            print(password)
            sql_cmd = sql_cmd.format(Id = 1, username=username, password=password, admin=admin, session_id=session_id)
            cur.execute(sql_cmd)
            conn.commit()

        else:
            sql_cmd = """
                Select *
                From Users
                Where username = '{username}'
            """
            sql_cmd = sql_cmd.format(username=username)
            cur.execute(sql_cmd)

            if self.dictfetchall(cur) != []:
                print('rejected')
                conn.close()
                return False
            password = generate_password_hash(password, 10).decode('utf8')
            print(password)
            session_id = uuid.uuid4().hex
            sql_cmd = """
                    INSERT INTO Users(username, password, admin, session_id)
                    VALUES('{username}', '{password}', {admin}, '{session_id}')
                """

            sql_cmd = sql_cmd.format(username=username, password=password, admin=admin, session_id=session_id)
            cur.execute(sql_cmd)
            conn.commit()

        conn.close()
        return True

    def updateUserPublicKey(self,username, publicKey, signaturePublicKey):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_cmd = """
            Select *
            From Users
            Where username = '{username}'
        """
        sql_cmd = sql_cmd.format(username=username)
        cur.execute(sql_cmd)

        if self.dictfetchall(cur) == []:
            conn.close()
            return False

        sql_query = """
            UPDATE Users
            SET publicKey = '{publicKey}', signaturePublicKey = '{signaturePublicKey}'
            WHERE username = '{username}';
        """
        sql_query = sql_query.format(publicKey=publicKey, signaturePublicKey=signaturePublicKey, username=username)
        cur.execute(sql_query)
        conn.commit()
        conn.close()
        return True

    def getUserPublicKey(self, username):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = """
            Select publicKey, signaturePublicKey
            From Users
            Where username = '{username}'
        """
        sql_query = sql_query.format(username=username)
        cur.execute(sql_query)
        publicKeyPair = self.dictfetchall(cur)
        return publicKeyPair

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = """
                SELECT password
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)
        cur.execute(sql_query)
        # If our query returns
        password_hashed = self.dictfetchall(cur)
        if password_hashed == []:
            return False

        password_hashed = password_hashed[0]["password"]
        #print(password_hashed)
        if check_password_hash(password_hashed, password) == True:
            session_id = uuid.uuid4().hex
            sql_query = """
                UPDATE Users
                SET session_id = '{session_id}'
                WHERE username = '{username}';
            """
            sql_query = sql_query.format(session_id=session_id, username=username)
            cur.execute(sql_query)
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    def check_session_id(self, session_id):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = """
                SELECT username
                FROM Users
                WHERE session_id = '{session_id}';
            """

        sql_query = sql_query.format(session_id=session_id)
        cur.execute(sql_query)
        current_user = self.dictfetchall(cur)
        return current_user

    def log_out(self, username):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = """
            UPDATE Users
            SET session_id = null
            WHERE username = '{username}';
        """
        sql_query = sql_query.format(username=username)
        cur.execute(sql_query)
        conn.commit()
        conn.close()
        return True

    def get_user_info(self, username):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = """
                Select *
                From Users
                Where username = '{username}'
            """
        sql_query = sql_query.format(username=username)
        cur.execute(sql_query)
        user_info = self.dictfetchall(cur)
        conn.close()
        return user_info


    def add_friends(self, user1_name, user2_name):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        user1_info = self.get_user_info(user1_name)
        user2_info = self.get_user_info(user2_name)
        user1_id = user1_info[0]["Id"]
        user2_id = user2_info[0]['Id']
        sql_cmd = """
                Select *
                From Friends
            """
        cur.execute(sql_cmd)

        if self.dictfetchall(cur) == []:
            sql_query = """
                        INSERT INTO Friends(user1_id, user1_name, user2_id, user2_name, communication_id)
                        VALUES({user1_id}, '{user1_name}', {user2_id}, '{user2_name}', {communication_id});
                    """
            sql_query = sql_query.format(user1_id=user1_id, user1_name=user1_name, user2_id=user2_id, user2_name=user2_name, communication_id=1)
        else:
            sql_query = """
                        INSERT INTO Friends(user1_id, user1_name, user2_id, user2_name)
                        VALUES({user1_id}, '{user1_name}', {user2_id}, '{user2_name}');
                    """
            sql_query = sql_query.format(user1_id=user1_id, user1_name=user1_name, user2_id=user2_id, user2_name=user2_name)
        cur.execute(sql_query)
        conn.commit()
        conn.close()
        return True


    def get_user_friends_name(self, username):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = '''
                SELECT user2_id as Id, user2_name as username
                From Friends
                Where user1_name = '{username}'
                Union
                SELECT user1_id as Id, user1_name as username
                From Friends
                Where user2_name = '{username}'
        '''
        sql_query = sql_query.format(username=username)

        cur.execute(sql_query)
        friends = self.dictfetchall(cur)
        conn.close()
        return friends

    def send_message(self, username, friend_name, message, iv, signature):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = '''
                SELECT communication_id
                From Friends
                Where (user1_name = '{username}' and user2_name = '{friend_name}') or (user2_name = '{username}' and user1_name = '{friend_name}')
        '''
        sql_query = sql_query.format(username=username, friend_name=friend_name)
        cur.execute(sql_query)
        communication_id = self.dictfetchall(cur)
        if communication_id == []:
            return False
        else:
            communication_id = communication_id[0]["communication_id"]

        sql_query = '''
                Insert into Communication
                values({communication_id}, '{message}', '{iv}', '{signature}', datetime('now', '8 hours'),'{username}', '{friend_name}')
        '''
        sql_query = sql_query.format(communication_id=communication_id, message=message, iv=iv, signature=signature, username=username, friend_name=friend_name)
        cur.execute(sql_query)
        conn.commit()
        conn.close()
        return True

    def get_message_history(self, username, friend_name):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = '''
                SELECT communication_id
                From Friends
                Where (user1_name = '{username}' and user2_name = '{friend_name}') or (user2_name = '{username}' and user1_name = '{friend_name}');
        '''
        sql_query = sql_query.format(username=username, friend_name=friend_name)
        cur.execute(sql_query)
        communication_id = self.dictfetchall(cur)
        if communication_id == []:
            return []
        else:
            communication_id = communication_id[0]["communication_id"]

        sql_query = '''
                Select *
                From Communication
                Where communication_id = {communication_id};
        '''
        sql_query = sql_query.format(communication_id=communication_id)
        cur.execute(sql_query)
        message_history = self.dictfetchall(cur)
        conn.close()
        return message_history

    def get_course_info(self):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = '''
                SELECT *
                From Course
        '''
        cur.execute(sql_query)
        course_detail = self.dictfetchall(cur)
        return course_detail

    def get_post(self, course_name):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = '''
                SELECT *
                From Post
                Where course_name = '{course_name}'
        '''
        sql_query = sql_query.format(course_name=course_name)
        cur.execute(sql_query)
        post_detail = self.dictfetchall(cur)
        return post_detail

    def get_comment(self):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = '''
                SELECT *
                From Comment
        '''
        cur.execute(sql_query)
        comment_detail = self.dictfetchall(cur)
        return comment_detail

    def get_user_list(self, username):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = '''
                SELECT *
                From Users
                Where username != '{username}'
        '''
        sql_query = sql_query.format(username=username)
        cur.execute(sql_query)
        users_list = self.dictfetchall(cur)
        return users_list

    def create_post(self, course_name, title, content):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = """
                    INSERT INTO Post(course_name, title, content)
                    VALUES('{course_name}', '{title}', '{content}');
                """
        sql_query = sql_query.format(course_name=course_name, title=title, content=content)
        cur.execute(sql_query)
        conn.commit()
        return True

    def create_comment(self, post_id, comment):
        conn = sqlite3.connect(self.database_arg, check_same_thread=False)
        cur = conn.cursor()
        sql_query = """
                    INSERT INTO Comment(post_id, comment)
                    VALUES('{post_id}', '{comment}');
                """
        sql_query = sql_query.format(post_id=post_id, comment=comment)
        cur.execute(sql_query)
        conn.commit()
        return True