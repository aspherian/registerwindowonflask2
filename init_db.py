import psycopg2 as psycopg2
import os

conn = psycopg2.connect(
    host="localhost",
    database="flask_db",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'])

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS userdata;')

cur.execute('CREATE TABLE userdata (id serial PRIMARY KEY,'
            'login varchar (150) NOT NULL,'
            'email varchar (50) NOT NULL,'
            'password varchar (50) NOT NULL,'
            'image varchar (150));'
            )

cur.execute('INSERT INTO userdata (login, email, password, image)'
            'VALUES (%s, %s, %s, %s)',
            ('test login',
             'test email',
             'test password',
             'test image')
            )

conn.commit()

cur.close()
conn.close()