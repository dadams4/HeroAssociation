# Daniel Adams
# postgresql database code in separate file

from datetime import date

import psycopg2
import psycopg2.extras

from lib.config import *

#Connecting to the database
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
	    conn.rollback()
		
	cur.close()
	
#Query the datbase to add a message with info
def add_message(name, day, age, message):
    conn = connectToPSQLDB()
    if conn == None:
        return None
        
    query_string = "insert into messageboard (name, day, age, message) VALUES (%s, %s, %s, %s);"
    queryDB(query_string, conn, select = False, args = (name, day, age, message))
    
    conn.close()
    return 0
    