import psycopg2
import psycopg2.extras

def check_user(user):
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='muctepkot', password='muctepkot', host='localhost')
        print('Postgres connected', user)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT token FROM users WHERE user_name = '%s'" % user)
        result = cur.fetchone()
        print(result)
        cur.close()
        conn.close()
        return result
    except psycopg2.Error as e:
        print('Postgres failed:{0}'.format(e))
        return 'Error'

def create_user(user, token):
    try:
        conn = psycopg2.connect(dbname='postapi_security', user='muctepkot', password='muctepkot', host='localhost')
    except psycopg2.Error as e:
        print('Postgres failed:{0}'.format(e))
    cur = conn.cursor()
    cur.execute("INSERT INTO users(id, user_name, token, disabled) VALUES (DEFAULT, '{0}', '{1}', DEFAULT)".format(user, token))
    conn.commit()
    cur.close()
    conn.close()
    return 'user created'

# try:
#     conn = psycopg2.connect(dbname='postapi_security', user='muctepkot', password='muctepkot', host='localhost')
#     print('Postgres connected')
# except psycopg2.Error as e:
#     print('Postgres failed:{0}'.format(e))
# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
# cur.close()
# conn.close()