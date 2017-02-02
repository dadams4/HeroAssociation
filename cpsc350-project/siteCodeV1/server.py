import os
#import psycopg2
#import psycopg2.extras
from flask import Flask, redirect, render_template, request

from lib.config import*
from lib import postgresql_data as pg

app = Flask(__name__)

wallPosts = [{'name': 'Andrew Jackson', 'date': '2017-01-27', 'message': 'I was the 7th President of the United States',
			'email': 'POTUS7@us.gov'}]

@app.route('/')
def mainIndex():
	theWeek = "Week Three"
	isWorking = True
	weeklySite = {'name': '/r/learnprogramming: ', 'description': 'A subreddit dedicated to learning and teaching programming'}
	myVideos = [{'title': 'Judge Morty: State of Georgia Vs. Rick Allen(WARNING: BAD LANGUAGE', 'link': 'WTWdP5DMdsM','description': 'A real courtcase reenacted by Rick and Morty(WARNING: BAD LANGUAGE)'},
	          {'title': 'Star Wars but every time someone shoots a laser it speeds up', 'link': 'wIIoMaidXq0', 'description': 'I needed a second video and this was suggested on the YouTube homepage'}]
	return render_template('index.html', week = theWeek, site = weeklySite, working = isWorking, videos = myVideos)


#Intermediate page between submitting to the database and the message board
@app.route('/thankyou', methods = ['GET', 'POST'])
def sendmessage():
	
	result = pg.add_message(request.form['name'], request.form['date'],	request.form['age'], request.form['message'])
	
	if result == None:
		return render_template('error.html')
		
	return render_template('sendinfo.html', yourName = request.form['name'])
	
	
#Displaying the messageboard
@app.route('/messageboard')
def messageboard():
	
	connection = pg.connectToPSQLDB()
	cur = connection.cursor()
	try:
		cur.execute("select * from messageboard")
	except:
		print("An error has occurred while trying to display messages.")
		
	
	results = cur.fetchall()
	#cur.close()
	return render_template('messageboard.html', posts=results)

# start the server
if __name__ == '__main__':
    
    #app.debug=True
    #app.run(host='0.0.0.0', port=8080)
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)