import md5
import os, binascii
import datetime
from flask import Flask, render_template, request, redirect, session, flash
app = Flask(__name__)
app.secret_key = 'jkfu890342htruo34v7yut8039pthjiopv78t0432-y5t3480wtb342y905n34um20w'

from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app, 'friendsdb')

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
@app.route('/users')
def index():
	query = "SELECT * FROM friends"
	users = mysql.query_db (query)
	return render_template('index.html', users=users)



app.run(debug=True)