#!/usr/bin/env python
import MySQLdb
import sys
import datetime
import time


#removes all records that are ALL -100 (completly bad record)


db=MySQLdb.connect("localhost","auto","myvice12","main")
curs=db.cursor()
curs.execute("select * from dt")
s=curs.fetchall()


for rec in s:
	if rec[2]==-100 and rec[3]==-100 and rec[4]==-100 and rec[5]==-100 and rec[6]==-100 and rec[7]==-100 and rec[8]==-100 and rec[9]==-100 and rec[10]==-100 and rec[11]==-100 and rec[12]==-100 and rec[13]==-100 and rec[14]==-100 and rec[15]==-100:
		print("Bad Record")
		curs.execute("delete from dt where id="+str(rec[16]))
		db.commit()
print("Closing Database and exiting")
db.close()
