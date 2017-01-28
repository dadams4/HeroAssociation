import os
from flask import Flask, render_template, request
app = Flask(__name__)

#names = ['']#['Dat boi', 'Kevin McMahon']
#dates = ['']#['01/25/2017','05/13/2012']
#messages = ['']#['I love this website!','This website is okay I guess...']

wallPosts = [{'name': 'Andrew Jackson', 'date': '2017-01-27', 'message': 'I was the 7th President of the United States',
			'email': 'POTUS7@us.gov'}]

@app.route('/')
def mainIndex():
	theWeek = "Week Two"
	isWorking = False
	weeklySite = {'name': '/r/learnprogramming: ', 'description': 'A subreddit dedicated to learning and teaching programming'}
	myVideos = [{'title': 'Judge Morty: State of Georgia Vs. Rick Allen(WARNING: BAD LANGUAGE', 'link': 'WTWdP5DMdsM','description': 'A real courtcase reenacted by Rick and Morty(WARNING: BAD LANGUAGE)'},
	          {'title': 'Star Wars but every time someone shoots a laser it speeds up', 'link': 'wIIoMaidXq0', 'description': 'I needed a second video and this was suggested on the YouTube homepage'}]
	return render_template('index.html', week = theWeek, site = weeklySite, working = isWorking, videos = myVideos)


@app.route('/messages', methods = ['POST'])
def sendmessage():
	
	wallPosts.append({'name': request.form['name'], 'date': request.form['date'], 'message': request.form['message'],
		'email': request.form['email']})
		
	return render_template('sendinfo.html', yourName = request.form['name'], posts = wallPosts)

# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
