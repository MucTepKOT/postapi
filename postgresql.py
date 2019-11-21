import psycopg2
import psycopg2.extras
import json
import time

def check_user(user):
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='muctepkot', password='muctepkot', host='localhost')
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
        conn = psycopg2.connect(dbname='postapi_security', user='muctepkot', password='muctepkot', host='localhost')
    except psycopg2.Error as err:
        print('Postgres failed:{0}'.format(err))
    cur = conn.cursor()
    timestamp = time.time()
    try:
        cur.execute("INSERT INTO users(id, user_name, password, token, time) VALUES (DEFAULT, '{0}', '{1}', '{2}', {3})".format(user, password, token, timestamp))
        conn.commit()
        return token
    except psycopg2.Error as err:
        print(str(err))
        return 'Error'
    cur.close()
    conn.close()

def get_token(user):
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='muctepkot', password='muctepkot', host='localhost')
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
        current_time = int(time.time())
        conn = psycopg2.connect(dbname='postapi_security', user='muctepkot', password='muctepkot', host='localhost')
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT time FROM users WHERE token = '%s'" % token)
        result = cur.fetchone()
        cur.close()
        conn.close()
        if current_time - result[0] > 3600:
            return False
        else:
            return True
    except psycopg2.Error as err:
        print('Postgres failed:{0}'.format(err))
        return 'Error'



    

# try:
#     conn = psycopg2.connect(dbname='postapi_security', user='muctepkot', password='muctepkot', host='localhost')
#     print('Postgres connected')
# except psycopg2.Error as e:
#     print('Postgres failed:{0}'.format(e))
# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
# cur.close()
# conn.close()