import os
import uuid
#import psycopg2
#import psycopg2.extras
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room

from lib.config import*
from lib import postgresql_data as pg

app = Flask(__name__)
#app = Flask(__name__, static_url_path='')

app.secret_key = os.urandom(24).encode('hex')

#-------------------Begin Chat stuff----------------------------------# 
#Chat stuff 
socketio = SocketIO(app)

messages = [{'text': 'Welcome to the chat!', 'name': 'Welcome Bot', 'room': 'Lobby'}]
            # {'text': 'IRC is better', 'name': 'DanBot'}]
searchedmessages = [{'text': 'Welcome to the chat!', 'name': 'Welcome Bot', 'room': 'Lobby'}]


users = {}
rooms = ['Lobby']



#Getting a list of the currently connected users
def updateList():
    
    usernames = []
    
    for user in users:
        
        #Checking if the user provided a name
        if len(users[user]['username']) == 0:
            usernames.append('Lurker')
        else:
            usernames.append(users[user]['username'])
    
    socketio.emit('list', usernames)
    
#Looking at the rooms    
def updateRooms():
    
    socketio.emit('rooms', rooms)
    #for room in rooms:
    #    print(room)
    
#Joining the chat room
@socketio.on('join')#, namespace='/iss')
def on_join(room):
    
    
	leave_room(users[session['uuid']]['room'])
    
	print('Leaving room ' + users[session['uuid']]['room'])
    
	join_room(room)
    
	users[session['uuid']]['room'] = room
    
	print(users[session['uuid']]['username'] + " Joined room" + room)
    
    #Getting the messages from the DB
	results = pg.get_chat()
	
	for result in results:
		
		tmp = {'text': result[0], 'room': result[1], 'name': result[2] }
		
		messages.append("{'text': " + "'" + result[0] + "'" + ", 'name': " + "'" + result[1] + "'" + ", 'room': " + "'" + result[2] + "'" + "}")
		
		#for message in messages:
		#	print (message)
		
		#print('result 0 ' + result[0] + ' result 1 '+ result[1] + ' result 2 ' + result[2])
	
		emit('message', tmp, room = result[1])

#Showing the messages from the searched for user
@socketio.on('search')
def on_search(username):
	
	name = username
	
	results = pg.get_specificChats(name)
	
	for result in results:
		
		tmp = {'text': result[0], 'room': result[1], 'name': result[2] }

		divider = {'text': '----------------', 'room': '----------------', 'name': 'Starting Searched Messages'}
		
		#emit('message', divider)

		emit('message', tmp)
	

#Adding messages to the webpage
@socketio.on('message')#, namespace='/iss')
def new_message(message):
    
    tmp = {'text': message['text'], 'room': message['room'], 'name': users[session['uuid']]['username']}
    print(tmp)
    pg.add_chatmessage(message['text'], message['room'], users[session['uuid']]['username'])
    messages.append(tmp)
    #print("Emitting to room " + message['room'])
   # for message in messages:
       # print("This is a message "+message)
    emit('message', tmp, room = message['room'])

#Handling user input
@socketio.on('identify')#, namespace='/iss')
def identify(message):
    
    #Checking to see if this particular computer has logged in
    if 'uuid' in session:
        users[session['uuid']]['username'] = message;
    
        print("identify " + users[session['uuid']]['username'])
    
        updateList()
    else:
        print('New user inc.')
        session['uuid'] = uuid.uuid1()
        users[session['uuid']] = {'username': 'New Chatter', 'room': 'Lobby'}
        join_room('Lobby')
        session['username'] = 'default'
        
        
        updateList()
        updateRooms()
        
    
#Create new room
@app.route('/new_room', methods=['Post'])
def create_room():
    rooms.append(request.get_json()['name'])
    print('updating rooms')
    updateRooms()
    return jsonify(success = "ok")

@socketio.on('disconnect')
def on_disconnect():
    if session['uuid'] in users:
        del users[session['uuid']]
        updateList()
        
        
"""
socketio = SocketIO(app)

messages = [{'text': 'test', 'name': 'DanBot'},
             {'text': 'IRC is better', 'name': 'DanBot'}]

users = {}

#connecting to socket
@socketio.on('connect', namespace='/iss')
def makeConnection():
    session['uuid'] = uuid.uuid1()
    session['username'] = 'New User'
    print('connected')
    users[session['uuid']] = {'username': 'New User'}
    
    for message in messages:
        print(message)
        emit('message', message)

#Adding messages to the webpage
@socketio.on('message', namespace='/iss')
def new_message(message):
    
    tmp = {'text': message, 'name': users[session['uuid']]['username']}
    print(tmp)
    messages.append(tmp)
    emit('message', tmp, broadcast=True)

#Handling user input
@socketio.on('identify', namespace='/iss')
def identify(message):
    print('identify ' + message)
    users[session['uuid']] = {'username': message}
    
    
    
#Join a room
@socketio.on('join')
def on_join(data):
	username = users[session['uuid']]
	room = data['room']
	join_room(room)
	emit(username + ' has entered the room.', room=room)
	
#Leave a room
@socketio.on('leave')
def on_leave(data):
	username = users[session['uuid']]
	room = data['room']
	leave_room(room)
	emit(username + ' has left the room.', room=room)
	"""
#------------------------End Chat Stuff------------------------------------------#			

logged = ''
loggedin = False
@app.route('/', methods = ['GET', 'POST'])
def mainIndex():
	
	if 'userName' in session:
		user = [session['userName'], session['password1']]
		
	else:
		user = ['','']
		
	theWeek = "Week Five"
	isWorking = True
	weeklySite = {'name': '/r/learnprogramming: ', 'description': 'A subreddit dedicated to learning and teaching programming'}
	myVideos = [{'title': 'Judge Morty: State of Georgia Vs. Rick Allen(WARNING: BAD LANGUAGE', 'link': 'WTWdP5DMdsM','description': 'A real courtcase reenacted by Rick and Morty(WARNING: BAD LANGUAGE)'},
	          {'title': 'Star Wars but every time someone shoots a laser it speeds up', 'link': 'wIIoMaidXq0', 'description': 'I needed a second video and this was suggested on the YouTube homepage'}]
	return render_template('index.html', week = theWeek, site = weeklySite, working = isWorking, videos = myVideos, logged = user)
	

@app.route('/login', methods = ['GET', 'POST'])
def createUser():
	
	if request.method == 'POST':
		session['userName'] = request.form['logusername']
		session['password1'] = request.form['logpassword']
		#session['loc'] = pg.get_location(session['userName'])
			
		
	#Crap we need to render shit
	theWeek = "Week Five"
	isWorking = True
	weeklySite = {'name': '/r/learnprogramming: ', 'description': 'A subreddit dedicated to learning and teaching programming'}
	myVideos = [{'title': 'Judge Morty: State of Georgia Vs. Rick Allen(WARNING: BAD LANGUAGE', 'link': 'WTWdP5DMdsM','description': 'A real courtcase reenacted by Rick and Morty(WARNING: BAD LANGUAGE)'},
	          {'title': 'Star Wars but every time someone shoots a laser it speeds up', 'link': 'wIIoMaidXq0', 'description': 'I needed a second video and this was suggested on the YouTube homepage'}]
	
	if 'userName' in session:
		user = [session['userName'], session['password1']]
	
	else:
		user = ['','']
	
	result = pg.get_user(session['userName'], session['password1'])
	
	if not result:
		session['userName'] = ''
		session['password1'] = ''
		return render_template('error.html')
	
	return render_template('index.html', week = theWeek, site = weeklySite, working = isWorking, videos = myVideos, logged = user)

#Creating an account 
@app.route('/createaccount', methods = ['GET', 'POST'])
def addaccount():
	
	if request.method == 'POST':
		session['userName'] = request.form['username']
		session['password1'] = request.form['password1']
		session['location'] = request.form['location']
		
	if 'userName' in session:
		user = [session['userName'], session['password1']]
		
	else:
		user = ['','']
		
	result = pg.add_user(session['userName'], session['password1'], session['location'])
	
	if result == None:
		session['userName'] = ''
		session['password1'] = ''
		return render_template('error.html')
		
	return render_template('createuser.html', logged = user)
#Intermediate page between submitting to the database and the message board
@app.route('/thankyou', methods = ['GET', 'POST'])
def sendmessage():
	
	if 'userName' in session:
		user = [session['userName'], session['password1']]
		
	else:
		user = ['','']
	
	result = pg.add_message(request.form['type'], request.form['perps'], request.form['date'], request.form['casualties'],
	request.form['criminal'], request.form['level'], request.form['location'])
	
	if result == None:
		return render_template('error.html')
		
	return render_template('sendinfo.html', logged = user)
	
#Displaying the messageboard
@app.route('/messageboard')
def messageboard():
	if 'userName' in session:
		user = [session['userName'], session['password1']]
		
	else:
		user = ['','']
	
	results = pg.get_messageboard()
	if not results:
		return render_template('error.html')
		
	return render_template('messageboard.html', posts=results, logged=user)



#Displaying specific crimes
@app.route('/search', methods = ['GET', 'POST'])
def searchcrimes():
		
	if 'userName' in session:
		user = [session['userName'], session['password1']]
		
	else:
		user = ['','']
	
	crimes = request.form['crimetype']
	results = pg.get_crimes(session['userName'], request.form['crimetype'])
	
	return render_template('crimes.html', posts=results, logged=user, crime = crimes)
	
#Chat Room	
@app.route('/chat', methods = ['GET', 'POST'])
def getchat():
	 print("working")
	 return app.send_static_file('chat.html')
	 
# start the server
if __name__ == '__main__':
    
    #app.debug=True
    #app.run(host='0.0.0.0', port=8080)
    #app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
