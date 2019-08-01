import os
from flask import render_template, request, redirect, session, url_for
from app import app
app.secret_key = b'\xb0\xb5\xdaqL\x81nm\xf7\x07\xd2\xbfi^\x80\xeb'

from flask_pymongo import PyMongo
# name of database
app.config['MONGO_DBNAME'] = 'bigdata' 
# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:bigtomato@cluster0-ibo92.mongodb.net/bigdata?retryWrites=true&w=majority' 
mongo = PyMongo(app)
# INDEX

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')
# CONNECT TO DB, ADD DATA
@app.route('/add')

def add():
    # connect to the database

    # insert new data

    # return a message to the user
    return ""
@app.route('/game')
def game():
    question = [{"question":"Bernie Sanders is a candiate?", "answer":"True"}]
    return render_template('game.html', question=question)

@app.route('/truth', methods=['POST','GET'])
def truth():
    question = [{"question":"Bernie Sanders is a candiate?", "answer":"True"}]
    if request.method == 'POST':
        if request.form['submit_button'] == question[0]["answer"]:
            answer ="goodjob"
        # elif request.form['submit_button'] == question[0]["answer"]:
        #     answer = "badjob"
        else:
            answer="badjob"
    elif request.method == 'GET':
        return render_template('game.html',answer=answer)
# Put watch and download buttons into your template:

@app.route('/signup', methods = ['GET', 'POST'])    
def signup():
    if request.method=='POST':
        realusers = mongo.db.realusers
        existing_user = realusers.find_one({'username':request.form['username']})
        if existing_user is None:
            realusers.insert({'username':request.form['username'],'password':request.form['password']})
            return "success"
        else:
            return "taken"
    else:
        return render_template('signup.html')
@app.route('/login', methods = ['POST'])    
def login():
        realusers = mongo.db.realusers
        existing_user = realusers.find_one({'username':request.form['username']})
        if existing_user:
            realusers.insert({'username':request.form['username'],'password':request.form['password']})
            if existing_user['password']==request.form['password']:
                session['username']=request.form['username']
                return redirect(url_for('index'))
            else:
                    return "your password doe'snt match your username"
        else:
            return "no existing user"
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
@app.route('/name/<username>')
def profile(username):
    realusers = mongo.db.realusers
    profiles = realusers.find({"username":username})
    return render_template('profile.html', profiles = profiles)
    
