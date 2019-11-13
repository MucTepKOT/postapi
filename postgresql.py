import psycopg2
import psycopg2.extras

try:
    conn = psycopg2.connect(dbname='postapi_security', user='muctepkot', password='muctepkot', host='localhost')
    print('Postgres connected')
except psycopg2.Error as e:
    print('Postgres failed:{0}'.format(e))

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

cur.execute("SELECT * FROM users")
result = cur.fetchall()
print(result)
cur.close()
conn.close()