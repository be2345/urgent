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
    any=question[0]
    return render_template('game.html', question=question,any=any)

# def stairsthree(floors):
#     steps = floors/floors
#     for steps in range(1,floors+1):
#         print(steps*"#")
# stairsthree(5)
cool=0
points=0
@app.route('/truth', methods=['POST','GET'])

def truth():
    question = [{"question":"Bernie Sanders is a candiate?", "answer":"False","points":100},{"question":"Joe Biden is a candiate?", "answer":"False","points":100},{"question":"Elizabeth Warren is a candiate?", "answer":"False","points":100},{"question":"Pete Buttigeg is a candiate?", "answer":"False","points":100},{"question":"Kamala Harris is a candiate?", "answer":"False","points":100}]
    global cool
    any= question[cool]
    global points
    answer=" "
    while cool <= 4:
    # count = 0
        if request.method == 'POST':
            if request.form['submit_button'] == question[cool]["answer"]:
                answer = "goodjob"
                points += 100
                interesting = points
                any=question[cool]
                cool+=1
                any=question[cool]
                # if request.method == 'POST':
                #     continue
                return render_template('game.html', answer=answer, question=question,any=any,interesting=interesting)
            # elif cool == 4:
            #     cool=0
            else:
                answer = "badjob"
                # points.append(-1*(question[cool]["points"]))
                points -=100
                interesting = points
                # cool=cool+1
                any=question[cool]
                cool+=1
                any= question[cool]
                # if request.method == 'POST':
                #     continue
                return render_template('game.html', answer=answer, question=question,any=any, intersting=interesting)
                # return render_template('game.html', answer=answer, question=question,any=any)
        elif request.method == 'POST':
            return render_template('game.html', answer=answer, question=question,any=any)
        elif cool ==4:
            cool=0
        else:
            return "goodbye"
 
          
            # elif request.form['value'] == question[0]["answer"]:
        #     answer = "badjob"
       
#  original_questions = {
#  #Format is 'question':[options]
#  'Taj Mahal':['Agra','New Delhi','Mumbai','Chennai'],
#  'Great Wall of China':['China','Beijing','Shanghai','Tianjin'],
#  'Petra':['Ma\'an Governorate','Amman','Zarqa','Jerash'],
#  'Machu Picchu':['Cuzco Region','Lima','Piura','Tacna'],
#  'Egypt Pyramids':['Giza','Suez','Luxor','Tanta'],
#  'Colosseum':['Rome','Milan','Bari','Bologna'],
#  'Christ the Redeemer':['Rio de Janeiro','Natal','Olinda','Betim']
# }

# questions = copy.deepcopy(original_questions)

# def shuffle(q):
#  """
#  This function is for shuffling 
#  the dictionary elements.
#  """
#  selected_keys = []
#  i = 0
#  while i < len(q):
#   current_selection = random.choice(q.keys())
#   if current_selection not in selected_keys:
#   selected_keys.append(current_selection)
#   i = i+1
#  return selected_keys

# @app.route('/')
# def quiz():
#  questions_shuffled = shuffle(questions)
#  for i in questions.keys():
#   random.shuffle(questions[i])
#  return render_template('main.html', q = questions_shuffled, o = questions)


# @app.route('/quiz', methods=['POST'])
# def quiz_answers():
#  correct = 0
#  for i in questions.keys():
#   answered = request.form[i]
#   if original_questions[i][0] == answered:
#   correct = correct+1
#  return '<h1>Correct Answers: <u>'+str(correct)+'</u></h1>'

# if __name__ == '__main__':
#  app.run(debug=True)  
# cool = 0
# @app.route('/truth', methods=['POST','GET'])
# def truth():
#     global cool
#     any = quiz.question[cool]
#     points = 0
#     answer1 = "Good Job"    
#     while cool < 4:
#         if request.form['submit_button'] == quiz.question[cool]['answer']:
#             points += 1
#             cool +=1
#             coolz = cool
#             print("cool points is"+str(cool))
#             # start_timer; start_loop
#             return render_template('game.html', answer=answer1, any= quiz.question[cool] )

#         else:
#             return "WRONG"
# Put watch and download buttons into your template:
# class myThread(threading.Thread):
#     def __init__(self, in_queue, out_queue):
#         threading.Thread.__init__(self)
#         self.in_queue = in_queue
#         self.out_queue = out_queue

#     def run(self):
#         while True:
#             item = self.in_queue.get() #blocking till something is available in the queue
#             #run your lines of code here
#             processed_data = item + str(datetime.now()) + 'Processed'
#             self.out_queue.put(processed_data)
# t = myThread(IN_QUEUE, OUT_QUEUE)


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
    
