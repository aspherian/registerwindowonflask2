import flask
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from werkzeug.utils import secure_filename
import psycopg2 as psycopg2
import os


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    return conn


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'


class RegisterForm(FlaskForm):
    login = StringField('Имя пользователя')
    email = StringField('Адрес электронной почты')
    password = StringField('Пароль')
    image = FileField()
    submit = SubmitField('Зарегистрироваться')


@app.route('/')
def index():
    return flask.redirect(flask.url_for('render'))


@app.route('/register/', methods=['GET', 'POST'])
def render():
    form = RegisterForm()
    if flask.request.method == 'GET':
        return render_template("index.html", form=form)
    filename = secure_filename(form.image.data.filename)
    form.image.data.save('static/img/' + filename)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO userdata (login, email, password, image)'
                'VALUES (%s, %s, %s, %s)',
                (form.login.data,
                 form.email.data,
                 form.password.data,
                 filename)
                )
    conn.commit()
    cur.close()
    conn.close()
    return render_template('registered.html', login=form.login.data, email=form.email.data, password=form.password.data,
                           imagename=filename)


if __name__ == '__main__':
    app.run()
