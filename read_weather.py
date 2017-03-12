#!/usr/bin/env python
import MySQLdb
import sys
import datetime
import time
def alert_scrub():
	
	#curs.execute("alter ignore table weather_alert add unique(body,expires)")
	#need to scrub for duplicates, hopefully keeping the newest one


	#Scrub for expired alerts	
	months=['Error','January','Feburary','March','April','May','June','July','August','September','October','November','December']
	#scrub the alert table and change 'active' status if needed
	curs.execute("select * from weather_alert where active=1")
	a=curs.fetchall()
	now=datetime.date.today()
	#print("Now")
	#print(now)
	rem=0
	for alert in a:
		#print(alert[3])
		r=str(alert[3])
		s=r.split('on')
		#print(s[1])	
		d=s[1].split(" ")
		day=d[2].split(',')
		yr=d[3]
		#print("Day: "+day[0])
		for x in range(1,13):
			if months[x]==d[1]:
				m=x
				#print("Found it")
				break
			print("Didnt Find Month...")
		print(yr+'-'+str(m)+'-'+day[0])
		if int(yr)<=now.year:
			if m<=now.month:
				if int(day[0])<now.day:
					rem+=1
					i=alert[8]
					print("ID: "+str(i))
					command='update weather_alert set active=0 where id='+str(i)+' limit 1'
					try:
						curs.execute(command)
						db.commit()
					except:
						print("Error Changing Entry: Rolling Back")
						db.rollback()
						print(sys.exc_info())
	print(str(rem)+" Expired")
db=MySQLdb.connect("localhost","auto","myvice12","main")
curs=db.cursor()

alert_scrub()

#fore=[]
curs.execute("select * from weather_forecast where fore_date=current_date()")
s=curs.fetchall()
#fore.append(s)
#curs.exectute("select * from weather_forecast where fore_date=current_date()+1")
#s=curs.fetchall()
#fore.append(s)
curs.execute("select * from weather_cur where rec_date=current_date() and city='albany' order by rec_time desc limit 1")
albany_cur=curs.fetchone() 

curs.execute("select * from weather_cur where rec_date=current_date() and city='portland' order by rec_time desc limit 1")
portland_cur=curs.fetchone() 

curs.execute("select * from weather_cur where rec_date=current_date() and city='salem' order by rec_time desc limit 1")
salem_cur=curs.fetchone() 

curs.execute("select * from weather_cur where rec_date=current_date() and city='eugene' order by rec_time desc limit 1")
eugene_cur=curs.fetchone() 


curs.execute("select * from weather_alert where active=1")
a=curs.fetchall()

albany_raw=[]
salem_raw=[]
portland_raw=[]
eugene_raw=[]
newport_raw=[]
for line in s:
	if line[16]=='albany':
		albany_raw.append(line)
	elif line[16]=='salem':
		salem_raw.append(line)
	elif line[16]=='portland':
		portland_raw.append(line)
	elif line[16]=='eugene':
		eugene_raw.append(line)
	else:
		continue
citys_raw=[]
citys_raw.append(albany_raw)
citys_raw.append(salem_raw)
citys_raw.append(portland_raw)
citys_raw.append(eugene_raw)
citys_cur=[]
citys_cur.append(albany_cur)
citys_cur.append(salem_cur)
citys_cur.append(portland_cur)
citys_cur.append(eugene_cur)	
citys_name=["Albany","Salem","Portland","Eugene"]
for x in range(0,4):
	#city_cur=citys_cur[x]
	high=0
	low=0
	wind=0
	wind_max=0
	qpf=0
	snow=0
	rain=0
	count=1
	scale=0
	for line in citys_raw[x]:
		high+=float(line[3])*.01*count
		low+=float(line[4])*.01*count
		snow+=float(line[14])*.01*count	
		qpf+=float(line[11])*.01*count
		wind+=float(line[5])*.01*count
		scale+=.01*count
		count+=1
	#compress 'rain' string to only four char
	rs=str(qpf/scale)
	rs=rs[:4]
	print(citys_name[x])
	print("\tForecast\tCurrent")
	print("Temp:\t"+str(int(high/scale))+"/"+str(int(low/scale))+"\t\t"+str(citys_cur[x][4]))
	print("Wind:\t"+str(int(wind/scale))+"\t\t"+str(citys_cur[x][5]))
	print("Rain:\t"+rs+"\t\t"+str(citys_cur[x][8]))
	print("Snow:\t"+str(snow/scale))
	for al in a:
		#print(al[7])
		if citys_name[x].lower()==al[7]:
			print(al[4]+" Expires: "+al[3])
			#print(al[5])
	
	print("\n")		


print("Closing Database and exiting")
db.close()
