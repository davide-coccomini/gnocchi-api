#ADD NEW ARCHIVE POLICY
import requests
import sys
import json
import subprocess
import re
from datetime import datetime, timedelta

#argv[1] = archive_policy_name
#argv[2] = granularity
#argv[3] = points

def get_token():
    global token
    global token_time
    p = subprocess.Popen('openstack token issue', shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0]
    m = re.search('id(.+?)project_id', str(output))
    if m:
        token = m.group(1)[11:-5]
        token_time = datetime.now()
        print(token)

def add_metric():
    global token
    global token_time
    if token == None or token_time < datetime.now() - timedelta(hours = 1):
        get_token()
    url = 'http://252.3.27.148:8041/v1/metric'
    data = {"archive_policy_name": str(sys.argv[1])}
    headers = {'Content-type': 'application/json', 'Content-Length':str(len(json.dumps(data))), 'X-Auth-Token':token}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r)

def add_policy():
    global token
    global token_time
    if token == None or token_time < datetime.now() - timedelta(hours = 1):
        get_token()
    url = 'http://252.3.27.148:8041/v1/archive_policy'
    data = {"back_window":0,"definition":[{"granularity":str(sys.argv[2]),"points":int(sys.argv[3])}],"name":str(sys.argv[1])}
    headers = {'Content-type': 'application/json', 'Content-Length':str(len(json.dumps(data))), 'X-Auth-Token':token}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r)
    add_metric()

token = None
token_time = None

add_policy()
