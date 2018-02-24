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
	query = "SELECT id, first_name, last_name, email, DATE_FORMAT(created_at, '%M %D, %Y') as created_at FROM friends"
	users = mysql.query_db (query)
	return render_template('index.html', users=users)


@app.route('/users/<id>')
def show(id):

	query = "SELECT * FROM friends WHERE id=:id"
	data = {'id': id}
	user = mysql.query_db (query, data)
	return render_template('show_user.html', user=user)

@app.route('/users/<id>', methods=['POST'])
def update(id):
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']

	query = "UPDATE friends SET first_name=:first_name, last_name=:last_name, email=:email, updated_at=NOW() WHERE id=:id"
	data = {
		'id': id,
		'first_name': first_name,
		'last_name': last_name,
		'email': email
	}

	mysql.query_db(query, data)


	return redirect('/users/' + str(id))

@app.route('/users/new')
def new():
	return render_template('new_user.html')


@app.route('/users/<id>/edit')
def edit(id):
	query = "SELECT first_name, last_name, email FROM friends WHERE id=:id"
	data= {'id': id}
	user = mysql.query_db(query,data)

	return render_template('edit_user.html', id=id, u=user[0])


@app.route('/users/create', methods=['POST'])
def create():
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']

	query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
	data = {
		'first_name': first_name,
		'last_name': last_name,
		'email': email
	}

	mysql.query_db(query, data)

	query = "SELECT id FROM friends WHERE first_name=:first_name AND last_name=:last_name AND email=:email"
	id = mysql.query_db(query, data)

	return redirect('/users/' + str(id[0]['id']))

@app.route("/users/<id>/destroy")
def destroy(id):
	query = "DELETE FROM friends WHERE id=:id"
	data = {'id': id}

	mysql.query_db(query, data)

	return redirect('/users')


app.run(debug=True)



