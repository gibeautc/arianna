#!/usr/bin/env python
import MySQLdb
import sys

db=MySQLdb.connect("localhost","auto","myvice12","main")
curs=db.cursor()
curs.execute("select * from weather_forecast where fore_date=current_date()")
s=curs.fetchall()
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
	elif line[16]=='newport':
		newport_raw.append(line)
	else:
		continue	
#Portland
high=0
low=0
wind=0
wind_max=0
qpf=0
snow=0
count=1
scale=0
for line in portland_raw:
	high+=float(line[3])*.01*count
	low+=float(line[4])*.01*count
	snow+=float(line[14])*.01*count	

	scale+=.01*count
	count+=1
print("Portland")
print("High: "+str(high/scale))
print("Low: "+str(low/scale))
print("Snow: "+str(snow/scale))
print("\n\n")


#Albany
high=0
low=0
wind=0
wind_max=0
qpf=0
snow=0
count=1
scale=0
for line in albany_raw:
	high+=float(line[3])*.01*count
	low+=float(line[4])*.01*count
	snow+=float(line[14])*.01*count	

	scale+=.01*count
	count+=1
print("Albany")
print("High: "+str(high/scale))
print("Low: "+str(low/scale))
print("Snow: "+str(snow/scale))

print("\n\n")


#Salem
high=0
low=0
wind=0
wind_max=0
qpf=0
snow=0
count=1
scale=0
for line in salem_raw:
	high+=float(line[3])*.01*count
	low+=float(line[4])*.01*count
	snow+=float(line[14])*.01*count	

	scale+=.01*count
	count+=1
print("Salem")
print("High: "+str(high/scale))
print("Low: "+str(low/scale))
print("Snow: "+str(snow/scale))
print("\n\n")

#Eugene
high=0
low=0
wind=0
wind_max=0
qpf=0
snow=0
count=1
scale=0
for line in eugene_raw:
	high+=float(line[3])*.01*count
	low+=float(line[4])*.01*count
	snow+=float(line[14])*.01*count	

	scale+=.01*count
	count+=1
print("Eugene")
print("High: "+str(high/scale))
print("Low: "+str(low/scale))
print("Snow: "+str(snow/scale))




print("Closing Database and exiting")
db.close()
