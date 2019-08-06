import os
from flask import render_template, request, redirect, session, url_for
from app import app
import threading
app.secret_key = b'\xb0\xb5\xdaqL\x81nm\xf7\x07\xd2\xbfi^\x80\xeb'
from app import quiz

from flask_pymongo import PyMongo
# name of database
app.config['MONGO_DBNAME'] = 'bigdata' 
# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:bigtomato@cluster0-ibo92.mongodb.net/bigdata?retryWrites=true&w=majority' 
mongo = PyMongo(app)
# INDEX
totalpoints=[]
totalquizzes=[]
totalcorrect=[]
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/gamesel')
def gamesel():
    return render_template('gamesel.html')
@app.route('/game')
def game():
    question = [{"question":"Bernie Sanders is a candiate?", "answer":"True"}]
    any=question[0]
    return render_template('game.html', question=question,any=any)
# cool=0
# points=0
# quiz_number=0
# @app.route('/truth', methods=['POST','GET'])
# def truth():
#     global cool
#     global quiz_number
#     any= quiz.question[quiz_number][cool]
#     global points
#     answer=" "
#     while cool <= 4:
#     # count = 0
#         if request.method == 'POST':
#             if request.form['submit_button'] == quiz.question[1][cool]["answer"]:
#                 answer = "goodjob"
#                 points += 100
#                 interesting = points
#                 # any=quiz.question[cool]
#                 cool+=1
#                 any=quiz.question[0][cool]
#                 if cool >= 4:
#                     cool=0
#                     return "Thank you"
#                 # if request.method == 'POST':
#                 #     continue
#                 else:
#                     return render_template('game.html', answer=answer, question=quiz.question[0],any=any,interesting=interesting)
#             # elif cool == 4:
#             #     cool=0
            
#             else:
#                 answer = "badjob"
#                 # points.append(-1*(question[cool]["points"]))
#                 points += -100
#                 interesting = points
#                 # cool=cool+1
#                 any= quiz.question[0][cool]
#                 cool+=1
#                 any= quiz.question[0][cool]
#                 if cool >= 4:
#                     cool=0
#                     return "Thank you"
#                 # if request.method == 'POST':
#                 #     continue
#                 else:
#                     return render_template('game.html', answer=answer, question=quiz.question[0],any=any, intersting=interesting)
#                 # return render_template('game.html', answer=answer, question=question,any=any)
#         elif request.method == 'POST':
#             return render_template('game.html', answer=answer, question=quiz.question[0],any=any)
        
#         else:
#             return "goodbye"
 
          
            # elif request.form['value'] == question[0]["answer"]:
        #     answer = "badjob"    

# def stairsthree(floors):
#     steps = floors/floors
#     for steps in range(1,floors+1):
#         print(steps*"#")
# stairsthree(5)

@app.route('/signup', methods = ['GET', 'POST'])    
def signup():
    if request.method=='POST':
        realusers = mongo.db.realusers
        existing_user = realusers.find_one({'username':request.form['username']})
        if existing_user is None:
            realusers.insert({'username':request.form['username'],'password':request.form['password']})
            return render_template('index.html')
        else:
            return "taken"
    else:
        return render_template('signup.html')
@app.route('/loginapp', methods = ['GET', 'POST'])    
def loginapp():
    answer=""
    if request.method=='POST':
        return render_template('login.html',answer=answer)
    else:
        return render_template('login.html',answer=answer)
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
                answer="Your Username did not match"
                return render_template('/login.html',answer=answer)
        else:
            answer="no existing user"
            return render_template('/login.html',answer=answer)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
@app.route('/name/<username>')
def profile(username):
    realusers = mongo.db.realusers
    profiles = realusers.find({"username":username})
    everpoints=sum(totalpoints)
    everquizzes=sum(totalquizzes)
    evercorrect=sum(totalcorrect)
    return render_template('profile.html', profiles = profiles,everpoints=everpoints,everquizzes=everquizzes,evercorrect=evercorrect)
any = quiz.question
quiz_number=0
colors=[]
cool=0
@app.route('/quiz/<quiz>', methods=['POST','GET'])
def gamer(quiz):
    global quiz_number
    # quiz_number=0
    global any
    global cool
    if request.method =='POST':
        del colors[:]
        cool=0
        quiz_number=int(request.form['submit_button'])-1
        # print(any)
        apple = any[quiz_number][0]
        # quiz=quiz.question[any]
        return render_template('gamer.html', apple=apple,colors=colors,cool=cool)
    else:
        return render_template('index.html', apple=apple,colors=colors,cool=cool)
        

points=0
pointslist=[0]
# quiz_number=0
@app.route('/truth', methods=['POST','GET'])
def truth():
    global cool
    global quiz_number
    apple= quiz.question[quiz_number][cool]
    global points
    answer=" "
    interesting = sum(pointslist)
    number=len(quiz.question[quiz_number])
    while cool <= 5:
    # count = 0
        if request.method == 'POST':
            if cool > 4:
                    cool=0
                    totalpoints.append(interesting)
                    totalquizzes.append(1)
                    totalcorrect.append(interesting/100)
                    del pointslist[:]
                    del colors[:]
                    return render_template('results.html',interesting=interesting, apple=apple,number=number)
            else:
                if request.form['submit_button'] == quiz.question[quiz_number][cool]["answer"]:
                    answer = "goodjob"
                    points += 100
                    pointslist.append(100)
                    interesting = sum(pointslist)
                    # any=quiz.question[cool]
                    cool+=1
                    apple=quiz.question[quiz_number][cool]
                    colors.append("green")
                    return render_template('gamer.html',colors=colors,cool=cool, answer=answer, question=quiz.question[quiz_number],apple=apple,interesting=interesting)
                    # if cool >= 6:
                    #     cool=0
                    #     totalpoints.append(interesting)
                    #     totalquizzes.append(1)
                    #     totalcorrect.append(interesting/100)
                    #     del pointslist[:]
                    #     del colors[:]
                    #     return render_template('results.html',interesting=interesting, apple=apple,number=number)
                    # # if request.method == 'POST':
                    # #     continue
                    # else:
                    #     return render_template('gamer.html',colors=colors,cool=cool, answer=answer, question=quiz.question[quiz_number],apple=apple,interesting=interesting)
                # elif cool == 4:
                #     cool=0
                elif request.form['submit_button'] == "Results":
                    cool+=1
                    return render_template('gamer.html',colors=colors,cool=cool, answer=answer, question=quiz.question[quiz_number],apple=apple,interesting=interesting)
                else:
                    answer = "badjob"
                    # points.append(-1*(question[cool]["points"]))
                    points += -100
                    interesting = points
                    interesting = sum(pointslist)
                    # cool=cool+1
                    cool+=1
                    apple= quiz.question[quiz_number][cool]
                    colors.append("red")
                    number=len(quiz.question[quiz_number])
                    return render_template('gamer.html',colors=colors,cool=cool, answer=answer, question=quiz.question[quiz_number],apple=apple,interesting=interesting)
                    # if cool >=6:
                    #     totalpoints.append(interesting)
                    #     del pointslist[:]
                    #     cool=0
                    #     del colors[:]
                    #     return render_template('results.html',interesting=interesting,number=number)
                    # # if request.method == 'POST':
                    # #     continue
                    # else:
                    #     return render_template('gamer.html',colors=colors,cool=cool, answer=answer, question=quiz.question[quiz_number],apple=apple, interesting=interesting)
                    # return render_template('game.html', answer=answer, question=question,any=any)

        elif request.method == 'POST':
            return render_template('gamer.html',colors=colors,cool=cool, answer=answer, question=quiz.question[quiz_number],apple=apple)
        
        else:
            return render_template('index.html') 
cany = quiz.choice
cquiz_number=0
ccolors=[]
ccool=0
@app.route('/mchoice/<mchoice>', methods=['POST','GET'])
def choice(mchoice):
    global cquiz_number
    # quiz_number=0
    global cany
    global ccool
    if request.method =='POST':
        del ccolors[:]
        ccool=0
        cquiz_number=int(request.form['submit_button'])-1
        # print(any)
        capple = cany[quiz_number][0]
        # quiz=quiz.question[any]
        return render_template('choice.html', apple=capple,colors=ccolors,cool=ccool)
    else:
        return render_template('index.html', apple=capple,colors=ccolors,cool=ccool)
        

cpoints=0
cpointslist=[0]
# quiz_number=0
@app.route('/choicetruth', methods=['POST','GET'])
def choicetruth():
    global ccool
    global cquiz_number
    capple= quiz.choice[cquiz_number][ccool]
    global cpoints
    answer=" "
    interesting = sum(cpointslist)
    number=len(quiz.choice[cquiz_number])
    while ccool <= 5:
    # count = 0
        if request.method == 'POST':
            if ccool > 4:
                    ccool=0
                    totalpoints.append(interesting)
                    totalquizzes.append(1)
                    totalcorrect.append(interesting/100)
                    del cpointslist[:]
                    del ccolors[:]
                    return render_template('results.html',interesting=interesting, apple=capple,number=number)
            else:
                if request.form['submit_button'] == quiz.choice[cquiz_number][ccool]["answer"]:
                    answer = "goodjob"
                    cpoints += 100
                    cpointslist.append(100)
                    interesting = sum(pointslist)
                    # any=quiz.question[cool]
                    ccool+=1
                    capple=quiz.choice[cquiz_number][ccool]
                    ccolors.append("green")
                    return render_template('choice.html',colors=ccolors,cool=ccool, answer=answer, question=quiz.choice[cquiz_number],apple=capple,interesting=interesting)
                    # if cool >= 6:
                    #     cool=0
                    #     totalpoints.append(interesting)
                    #     totalquizzes.append(1)
                    #     totalcorrect.append(interesting/100)
                    #     del pointslist[:]
                    #     del colors[:]
                    #     return render_template('results.html',interesting=interesting, apple=apple,number=number)
                    # # if request.method == 'POST':
                    # #     continue
                    # else:
                    #     return render_template('gamer.html',colors=colors,cool=cool, answer=answer, question=quiz.question[quiz_number],apple=apple,interesting=interesting)
                # elif cool == 4:
                #     cool=0
                elif request.form['submit_button'] == "Results":
                    ccool+=1
                    return render_template('choice.html',colors=ccolors,cool=ccool, answer=answer, question=quiz.choice[cquiz_number],apple=capple,interesting=interesting)
                else:
                    answer = "badjob"
                    # points.append(-1*(question[cool]["points"]))
                    cpoints += -100
                    interesting = points
                    interesting = sum(cpointslist)
                    # cool=cool+1
                    ccool+=1
                    apple= quiz.choice[cquiz_number][ccool]
                    ccolors.append("red")
                    number=len(quiz.choice[cquiz_number])
                    return render_template('choice.html',colors=ccolors,cool=ccool, answer=answer, question=quiz.choice[cquiz_number],apple=capple,interesting=interesting)
                    # if cool >=6:
                    #     totalpoints.append(interesting)
                    #     del pointslist[:]
                    #     cool=0
                    #     del colors[:]
                    #     return render_template('results.html',interesting=interesting,number=number)
                    # # if request.method == 'POST':
                    # #     continue
                    # else:
                    #     return render_template('gamer.html',colors=colors,cool=cool, answer=answer, question=quiz.question[quiz_number],apple=apple, interesting=interesting)
                    # return render_template('game.html', answer=answer, question=question,any=any)

        elif request.method == 'POST':
            return render_template('choice.html',colors=ccolors,cool=ccool, answer=answer, question=quiz.choice[cquiz_number],apple=capple)
        
        else:
            return render_template('index.html') 
          
            # elif request.form['value'] == question[0]["answer"]:
        #     answer = "badjob"
       


