from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re,os
app = Flask(__name__)
app.secret_key = os.urandom(32)
mysql = MySQLConnector(app,'mydb')
emailRegex = re.compile(r'^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-z]')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/addEmail',methods=['POST'])
def addEmail():
    query = 'INSERT INTO emails (email,created_at) VALUES (:email,NOW())'
    data = {'email':request.form['email']}
    if not emailRegex.match(request.form['email']):
        flash('Invalid email address')
        return redirect('/')
    else:
        mysql.query_db(query,data)
        emails = mysql.query_db('SELECT email,created_at FROM emails')
        return render_template('success.html',emailOut = data['email'],emailList = emails)
app.run(debug=True)
