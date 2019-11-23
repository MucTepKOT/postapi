import psycopg2
import psycopg2.extras
import json
import time

def check_user(user):
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='kot', password='kot', host='localhost')
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE user_name = '%s')" % user)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
    except psycopg2.Error as err:
        print(str(err))

def create_user(user, password, token):
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='kot', password='kot', host='localhost')
    except psycopg2.Error as err:
        print('Postgres failed:{0}'.format(err))
    cur = conn.cursor()
    current_time = int(time.time())
    try:
        cur.execute("INSERT INTO users(id, user_name, password, token, time) VALUES (DEFAULT, '{0}', '{1}', '{2}', {3})".format(user, password, token, current_time))
        conn.commit()
        return token
    except psycopg2.Error as err:
        print(str(err))
        return 'Error'
    cur.close()
    conn.close()

def get_token(user):
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='kot', password='kot', host='localhost')
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT token FROM users WHERE user_name = '%s'" % user)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
    except psycopg2.Error as err:
        print('Postgres failed:{0}'.format(err))
        return 'Error'

def token_alive(token):
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='kot', password='kot', host='localhost')
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT time FROM users WHERE token = '%s'" % token)
        result = cur.fetchone()
        cur.close()
        conn.close()
        current_time = int(time.time())
        if current_time - result[0] > 60:
            return False
        else:
            return True
    except psycopg2.Error as err:
        print('Postgres failed:{0}'.format(err))
        return 'Error'

def update_token(user, token):
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='kot', password='kot', host='localhost')
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        current_time = int(time.time())
        cur.execute("UPDATE users SET token = '%s' WHERE user_name = '%s'" % (token, user))
        cur.execute("UPDATE users SET time = '%s' WHERE user_name = '%s'" % (current_time, user))
        conn.commit()
        cur.close()
        conn.close()
        return 'Success'        
    except psycopg2.Error as err:
        print('Postgres failed:{0}'.format(err))
        return 'Error'

def check_password(user):
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='kot', password='kot', host='localhost')
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT password FROM users WHERE user_name = '%s'" % user)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
    except psycopg2.Error as err:
        print('Postgres failed:{0}'.format(err))
        return 'Error'
