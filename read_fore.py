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
			#print("Didnt Find Month...")
		#print(yr+'-'+str(m)+'-'+day[0])
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

#alert_scrub()

class ten_day(object):
	high=[]
	low=[]
	wind=[]
	rain=[]
	snow=[]
	weather=[]
	city=""
	def __init__(self,c):
		self.city=c
	def add_day(self,h,l,w,r,s,we):
		self.high.append(h)
		self.low.append(l)
		self.wind.append(w)
		self.rain.append(r)
		self.snow.append(s)
		self.weather.append(we)
	def Print(self):
		if len(self.high)!=10:
			print("Length error")
			print(len(self.high))
			return
		tabs=[]
		for l in self.weather:
			if len(l)<8:
				tabs.append("\t")
			else:
				tabs.append("\t\t")
			
		print("Weather for: "+self.city)
		print("Weather"+"\t"+self.weather[0]+"\t"+self.weather[1]+"\t"+self.weather[2]+"\t"+self.weather[3]+"\t"+self.weather[4])
		temp=[]
		for x in range(9):
			temp.append(str(self.high[x])+"/"+str(self.low[x]))	
			self.rain[x]=self.rain[x][:4]	
			self.wind[x]=self.wind[x][:4]	
			self.snow[x]=self.snow[x][:4]	

		print("Temp"+"\t"+temp[0]+tabs[0]+temp[1]+tabs[1]+temp[2]+tabs[3]+temp[3]+tabs[4]+temp[4])	
		print("Wind"+"\t"+self.wind[0]+tabs[0]+self.wind[1]+tabs[1]+self.wind[2]+tabs[3]+self.wind[3]+tabs[4]+self.wind[4])
		print("Rain"+"\t"+self.rain[0]+tabs[0]+self.rain[1]+tabs[1]+self.rain[2]+tabs[3]+self.rain[3]+tabs[4]+self.rain[4])
		print("Snow"+"\t"+self.snow[0]+tabs[0]+self.snow[1]+tabs[1]+self.snow[2]+tabs[3]+self.snow[3]+tabs[4]+self.snow[4])


def process_forcast(name):

	curs.execute("select * from weather_forecast where city='"+name+"' and fore_date>=current_date()")
	data=curs.fetchall()
	dates=[]
	forcast=[]
	for line in data:
		date=line[2]
		#will the dates always be in order????????
		if date not in dates:
			dates.append(date)
			t=[]
			forcast.append(t)
		i=dates.index(date)
		forcast[i].append(line)
		#print(i)
	#print(dates)
	#for line in forcast[9]:
		#print(line)
	tenday=ten_day(forcast[0][0][16])
	for day in forcast:
		high=0
		low=0
		wind=0
		rain=0
		snow=0
		count=0
		#day has all city data for 1 day
		#print("next day")
		for entry in day:
			#entry should be a single report
			#print(entry)
			high+=entry[3]
			low+=entry[4]
			rain+=entry[11]
			snow+=entry[14]
			wind+=entry[5]
			count+=1
			w=entry[15]
			#w="none"
		high=high/count
		low=low/count
		rain=rain/count
		snow=snow/count
		wind=wind/count
		tenday.add_day(str(high),str(low),str(wind),str(rain),str(snow),w)
	return tenday


#curs.execute("select * from weather_forecast where city='salem' and fore_date>=current_date()")
#s=curs.fetchall()
albany=process_forcast('albany')
albany.Print()

salem=process_forcast('salem')
salem.Print()

portland=process_forcast('portland')
portland.Print()


#	for line in citys_raw[x]:
#		high+=float(line[3])*.01*count
#		low+=float(line[4])*.01*count
#		snow+=float(line[14])*.01*count	
#		qpf+=float(line[11])*.01*count
#		wind+=float(line[5])*.01*count
#		scale+=.01*count
#		count+=1


print("Closing Database and exiting")
db.close()
