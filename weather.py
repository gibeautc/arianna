#!/usr/bin/env python
import subprocess
import time
import json
import urllib
import pprint
print("Getting Albany Weather")


city='albany'

#current conditions
#url="http://api.wunderground.com/api/803ee257021d3c0e/conditions/q/OR/"+city+".json"

#10 day forcast
url="http://api.wunderground.com/api/803ee257021d3c0e/forecast10day/q/OR/"+city+".json"


response=urllib.urlopen(url)
data=json.loads(response.read())
#print(data)
pp=pprint.PrettyPrinter(indent=2)
pp.pprint(data)
#location=data['current_observation']['display_location']['city']
#temp_f=data['current_observation']['temp_f']
#print("current temp in "+location+" is "+str(temp_f))

