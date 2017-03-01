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
	return results
	
#Query the datbase to add a message with info
def add_message(crimeType, criminalNumber, crimeDate, casualties, criminalName, threatLevel, crimeLocation):
    conn = connectToPSQLDB()
    if conn == None:
        return None
        
    query_string = "insert into crimes (crimeType, criminalNumber, crimeDate, casualties, criminalName, threatLevel, crimeLocation) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    queryDB(query_string, conn, select = False, args = (crimeType, criminalNumber, crimeDate, casualties, criminalName, threatLevel, crimeLocation))
    
    conn.close()
    return 0
    
#Query the database to add a user
def add_user(username, password, location):
	conn = connectToPSQLDB()
	if conn == None:
		return None
		
		
	#Checking if the username has been taken
	#user_string = "select username from users where username like %s"
	#queryDB(user_string, conn, select = False, args = (name))
	
	
	#If the username was not taken, go ahead and like insert it or shit
	query_string = "insert into users (username, password, location) VALUES (%s, crypt(%s, gen_salt('bf')), %s);"
	queryDB(query_string, conn, select = False, args = (username, password, location))
	
	conn.close()
	return 0

#Query to find users
def get_user(username, password):
	
	conn = connectToPSQLDB()
	if conn == None:
		return None
		
	query_string = "select username from users where username = %s and password = crypt(%s, password)"
	print(query_string)
	
	results = queryDB(query_string, conn, args = (username, password))
	print(results)
	conn.close()
	return results

#Query to get the location
def get_location(username):

	conn = connectToPSQLDB()
	if conn == None:
		return None
		
	query_string = "select location from users where username = %s"
	#print(query_string)
	results = queryDB(query_string, conn, args = (username,))
#	print(results)
	conn.close()
	return results


#Display the contents of the messageboard
def get_messageboard():

	conn = connectToPSQLDB()
	if conn == None:
		return None
	query_string = "select * from crimes"
	results = queryDB(query_string, conn)
	conn.close()
	return results

#Display crimes based on location
def get_crimes(username, crime):
	
	location = get_location(username)
	location = unicode(location[0])
	location = location[2:-2]
	print(crime)
	print(location)
	print(username)
	
	print(type(crime))
	print(type(username))
	print(type(location))
	conn = connectToPSQLDB()
	if conn == None:
		return None
	query_string = "select * from crimes where crimetype = %s and crimelocation = %s"
	print(query_string)
	results = queryDB(query_string, conn, args =(crime, location))
	print("get crimes")
	print(results)
	conn.close()
	return results