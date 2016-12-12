#!/usr/bin/env python
import requests
import re
import sys
from pprint import pprint
import json
at = "68ea42109ec80134adf205b7f1deccdf"  # this is a global variable that stores the API token
test_ID='27306241'
url_send='https://api.groupme.com/v3/groups/'+test_ID+'/messages?token='+at
message='Fuck+off+jason'
url='https://api.groupme.com/v3/bots/post?bot_id=481baace72a55ebbb9488e296e&text='+message
print(url)
r=requests.post(url)
print(r)
	
