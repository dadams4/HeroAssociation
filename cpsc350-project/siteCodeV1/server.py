#import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request
app = Flask(__name__)

#names = ['']#['Dat boi', 'Kevin McMahon']
#dates = ['']#['01/25/2017','05/13/2012']
#messages = ['']#['I love this website!','This website is okay I guess...']

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


@app.route('/thankyou', methods = ['POST'])
def sendmessage():
	
	conn = connectToDB()
	cur = conn.cursor()
#	name = request.form['name']
#	day = request.form['date']
#	age = request.form['age']
#	msg = request.form['message']
	try:
		cur.execute("""INSERT INTO messageboard (name, day, age, message) 
       VALUES (%s, %s, ,%d, %s);""",
       (request.form['name'], request.form['date'], request.form['age'], request.form['message']) )
#		cur.execute("insert into messageboard (name, day, age, message) VALUES (%s, %s, %d, %s)" % name , day, age, msg)
	except:
		print("error inserting")
		conn.rollback()
	
	conn.commit()
	
	#return render_template('messageboard.html', posts = results)
#	wallPosts.append({'name': request.form['name'], 'date': request.form['date'], 'message': request.form['message'],
#		'email': request.form['email']})
		
	return render_template('sendinfo.html', yourName = request.form['name'])

#Connecting to our database
def connectToDB():
	
	connectionString = 'dbname=siteinfo user=manager password=Daniel21 host=localhost'
	print connectionString
	try:
		return psycopg2.connect(connectionString)
	except:
		print("Unable to connect to the database")

@app.route('/messageboard')
def messageboard():
	
	connection = connectToDB()
	cur = connection.cursor()
	try:
		cur.execute("select * from messageboard")
	except:
		print("An error has occurred while trying to display messages.")
		
	results = cur.fetchall()
	return render_template('messageboard.html', posts=results)

# start the server
if __name__ == '__main__':
    
    app.debug=True
    app.run(host='0.0.0.0', port=8080)
    #app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
