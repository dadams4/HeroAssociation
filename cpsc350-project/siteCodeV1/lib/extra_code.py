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
	
def connectToPSQLDB():
    connectionString = 'dbname=%s user=%s password=%s host=%s' % (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST)
    print connectionString
    try:
    	return psycopg2.connect(connectionString)
    except Exception as e:
        print(type(e))
        print(e)
        print("Can't connect to database")
        return None
#Code that performs the actual query
def queryDB(query, conn, select=True, args=None):
    print("Executing a query")
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    results = None
    try:
        quer = cur.mogrify(query, args)
        cur.execute(quer)
        if select:
        	results = cur.fetchall()
        
    	conn.commit()
       
	except Exception as e:
    	conn.rollback()
        print(type(e))
        print(e)
    
    cur.close()
    return results
    
#Query the datbase to add a message with info
def add_message(name, day, age, message):
    conn = connectToPSQLDB()
    if conn == None:
    	return None
    query_string = "insert into messageboard (name, day, age, message) VALUES (%s, %s, %s, %s);"
    queryDB(query_string, conn, select = False, args = (name, day, age, message))
    
    conn.close()
    return 0
	
def get_messageboard():
    conn = connectToPSQLDB()
    if conn == None:
    	return None
    query_string = "select * from messageboard"
    results = queryDB(query_string, conn)
    conn.close()
    return results