import psycopg2
import psycopg2.extras
import json
import time
import logging

log_format = '%(asctime)s %(filename)s: %(message)s'
logging.basicConfig(filename="server.log", format=log_format, level=logging.DEBUG)

def postgres_conn():
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='muctepkot', password='muctepkot', host='localhost')
        return conn
    except psycopg2.DatabaseError as err:
        logging.error(f'PostgreSQL connection error: {str(err)}')


def check_user(user):
    try:
        conn = postgres_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE user_name = '%s')" % user)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
    except psycopg2.Error as err:
        print(str(err))
        logging.error(f'PostgreSQL error: {str(err)}')

def create_user(user, password, token):
    try:
        conn = postgres_conn()
        cur = conn.cursor()
        current_time = int(time.time())
        cur.execute("INSERT INTO users(id, user_name, password, token, time) VALUES (DEFAULT, '{0}', '{1}', '{2}', {3})".format(user, password, token, current_time))
        conn.commit()
        return token
    except psycopg2.Error as err:
        print(str(err))
        logging.error(f'PostgreSQL error: {str(err)}')
        return 'Error'
    cur.close()
    conn.close()

def get_token(user):
    try:
        conn = postgres_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT token FROM users WHERE user_name = '%s'" % user)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
    except psycopg2.Error as err:
        print('Postgres failed:{0}'.format(err))
        logging.error(f'PostgreSQL error: {str(err)}')
        return 'Error'

def token_alive(token):
    try:
        conn = postgres_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT time FROM users WHERE token = '%s'" % token)
        result = cur.fetchone()
        cur.close()
        conn.close()
        current_time = int(time.time())
        if current_time - result[0] > 3600:
            return False
        else:
            return True
    except psycopg2.Error as err:
        print('Postgres failed:{0}'.format(err))
        logging.error(f'PostgreSQL error: {str(err)}')
        return 'Error'

def update_token(user, token):
    try:
        conn = postgres_conn()
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
        logging.error(f'PostgreSQL error: {str(err)}')
        return 'Error'

def check_password(user):
    try:
        conn = postgres_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT password FROM users WHERE user_name = '%s'" % user)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
    except psycopg2.Error as err:
        print('Postgres failed:{0}'.format(err))
        logging.error(f'PostgreSQL error: {str(err)}')
        return 'Error'
