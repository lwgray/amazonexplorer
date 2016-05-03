import sqlite3 as sql
from flask import Flask, request, session, g, redirect,\
    url_for, abort, render_template, flash
from flask_bootstrap import Bootstrap
from flask.ext.uploads import configure_uploads
from flask.ext.uploads import UploadSet, AllExcept, SCRIPTS, EXECUTABLES


# Setup Upload folder
documents = UploadSet('documents', AllExcept(SCRIPTS + EXECUTABLES))

# configuration
DATABASE = 'tmp/explorer.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# Create flask application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOADS_DEFAULT_DEST'] = ''
# Setup Database, bootstrap, login, analytics
Bootstrap(app)
configure_uploads(app, documents)
# Setup Database, bootstrap, login, analytics
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.route('/')
@app.route('/index')
@app.route('/refunded')
def index():
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from refunds")
    rows = cur.fetchall();
    return render_template('refunded.html', rows=rows)


@app.route('/damaged')
def damaged():
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from damaged")
    rows = cur.fetchall();
    return render_template('damaged.html', rows=rows)


@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5111)
