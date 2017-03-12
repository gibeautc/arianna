#!/usr/bin/env python
import MySQLdb
import sys
import datetime
import time



db=MySQLdb.connect("localhost","auto","myvice12","main")
curs=db.cursor()


if len(sys.argv)>1:
	try:
		ID=int(sys.argv[1])
	except:
		print("not a number")
	curs.execute("select * from weather_alert where id="+str(ID))
	s=curs.fetchone()
	for field in s:
		print(field)
	#print(s[3])
	#print(s[4])
	#print(s[5])


print("Closing Database and exiting")
db.close()
