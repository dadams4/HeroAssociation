import os
#import psycopg2
#import psycopg2.extras
from flask import Flask, redirect, render_template, request, session

from lib.config import*
from lib import postgresql_data as pg

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

wallPosts = [{'name': 'Andrew Jackson', 'date': '2017-01-27', 'message': 'I was the 7th President of the United States',
			'email': 'POTUS7@us.gov'}]
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
# start the server
if __name__ == '__main__':
    
    #app.debug=True
    #app.run(host='0.0.0.0', port=8080)
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)