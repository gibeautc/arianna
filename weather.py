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

#current conditions
#url="http://api.wunderground.com/api/803ee257021d3c0e/conditions/q/OR/"+city+".json"
while True:
#10 day forcast
	url="http://api.wunderground.com/api/803ee257021d3c0e/forecast10day/q/OR/"+city[c_index]+".json"

	print("Updating: "+city[c_index])
	try:
		response=urllib.urlopen(url)
		data=json.loads(response.read())
	except:
		print("Error Getting Data")
		continue
	#print(data)
	#pp=pprint.PrettyPrinter(indent=2)
	forcast=data['forecast']['simpleforecast']['forecastday']
	for day in forcast:
		status=day['conditions']
		high=day['high']['fahrenheit']
		low=day['low']['fahrenheit']
		wind_mph=day['avewind']['mph']
		wind_dir=day['avewind']['dir']
		wind_max=day['maxwind']['mph']
		wind_mdir=day['maxwind']['dir']
		date_day=day['date']['day']
		date_month=day['date']['month']
		date_year=day['date']['year']
		snow_day=day['snow_day']['in']
		snow_night=day['snow_night']['in']
		snow_total=day['snow_allday']['in']
		qpf_day=day['qpf_day']['in']
		qpf_night=day['qpf_night']['in']
		qpf_total=day['qpf_allday']['in']
		#sql date format YYYY-MM-DD
		#Will need to check if single digit day and month are right
		db_date=str(date_year)+"-"+str(date_month)+"-"+str(date_day)
		db_out=[db_date,str(high),str(low),str(wind_mph),wind_dir,str(wind_max),wind_mdir,str(qpf_day),str(qpf_night),str(qpf_total),str(snow_day),str(snow_night),str(snow_total),status,city[c_index]]
		try:
			curs.execute('insert into weather_forecast values(current_date(),now(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',db_out)
			db.commit()
		except:
			print("Error: Rolling Back")
			db.rollback()
			print(sys.exc_info())
	c_index+=1
	if c_index==len(city):
		c_index=0
	time.sleep(200)
