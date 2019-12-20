import psycopg2
import psycopg2.extras
import json
import time
import logging
import yaml

try:
    with open(r'config.yaml') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)
        logging.info('Config successfully loaded')
except yaml.error.YAMLError as err:
    logging.error(f'Yaml config error: {err}')
    
log_format = '%(asctime)s %(filename)s: %(message)s'
logging.basicConfig(filename="server.log", format=log_format, level=logging.DEBUG)

def postgres_conn():
    try:
        conn = psycopg2.connect(dbname=config['psql_dbname'], user=config['psql_user'], password=config['psql_password'], host=config['psql_host'])
        logging.info(f'PostgreSQL connected')
        return conn
    except psycopg2.DatabaseError as err:
        logging.error(f'PostgreSQL connection error: {str(err)}')


def check_user(user):
    try:
        conn = postgres_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE user_name = '{user}')")
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
        cur.execute(f"INSERT INTO users(id, user_name, password, token, time) VALUES (DEFAULT, '{user}', '{password}', '{token}', {current_time})")
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
        cur.execute(f"SELECT token FROM users WHERE user_name = '{user}'")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
    except psycopg2.Error as err:
        print(f'Postgres failed:{err}')
        logging.error(f'PostgreSQL error: {str(err)}')
        return 'Error'

def token_alive(token):
    try:
        conn = postgres_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f"SELECT time FROM users WHERE token = '{token}'")
        result = cur.fetchone()
        cur.close()
        conn.close()
        current_time = int(time.time())
        if current_time - result[0] > 3600:
            return False
        else:
            return True
    except psycopg2.Error as err:
        print(f'Postgres failed:{err}')
        logging.error(f'PostgreSQL error: {str(err)}')
        return 'Error'

def update_token(user, token):
    try:
        conn = postgres_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        current_time = int(time.time())
        cur.execute(f"UPDATE users SET token = '{token}' WHERE user_name = '{user}'")
        cur.execute(f"UPDATE users SET time = '{current_time}' WHERE user_name = '{user}'")
        conn.commit()
        cur.close()
        conn.close()
        return 'Success'        
    except psycopg2.Error as err:
        print(f'Postgres failed:{err}')
        logging.error(f'PostgreSQL error: {str(err)}')
        return 'Error'

def check_password(user):
    try:
        conn = postgres_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f"SELECT password FROM users WHERE user_name = '{user}'")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0]
    except psycopg2.Error as err:
        print(f'Postgres failed:{err}')
        logging.error(f'PostgreSQL error: {str(err)}')
        return 'Error'
