# Code for adding to database (unsafe version)
"""
	conn = connectToDB()
	cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
	try:
		cur.execute(insert into messageboard (name, day, age, message) VALUES (%s, %s, %s, %s);, 
			(request.form['name'], 
			request.form['date'],
			int(request.form['age']), 
			request.form['message']))
	except:
		print("error inserting")
		print("Tried: INSERT INTO messageboard (name, day, age, message) VALUES ('%s', '%s', %d, '%s');" %
        	(request.form['name'], str(request.form['date']), int(request.form['age']), request.form['message']) )
        	
		conn.rollback()
		
	conn.commit()
	conn.close()
	return render_template('sendinfo.html', yourName = request.form['name'])
	"""