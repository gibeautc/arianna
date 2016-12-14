#!/usr/bin/env python
import subprocess
import time
import json
import urllib
import pprint
import MySQLdb
import sys
db=MySQLdb.connect('localhost','auto','myvice12','main')
curs=db.cursor()
print("Getting Albany Weather")
c_index=0
city=['albany','salem','portland','newport','eugene']
while True:
#alerts
	url="http://api.wunderground.com/api/803ee257021d3c0e/alerts/q/OR/"+city[c_index]+".json"
	try:
		response=urllib.urlopen(url)
		data=json.loads(response.read())
		alerts=data['alerts']
	except:
		print("Error Getting Data")
		continue
	for alert in alerts:
		issued=alert['date']
		description=alert['description']
		expires=alert['expires']
		message=alert['message']
		print("Alerts for: "+city[c_index])
		print(issued)
		print("Expires: "+expires)
		print(description)
		print(message)
		db_out=[str(issued),str(expires),str(description),str(message),str(1),city[c_index]]
		try:
			curs.execute('insert into weather_alert values(current_date(),now(),%s,%s,%s,%s,%s,%s)',db_out)
			db.commit()
		except:
			print("Error: Rolling Back")
			db.rollback()
			print(sys.exc_info())
	c_index+=1
	if c_index==len(city):
		c_index=0
	time.sleep(2000)
