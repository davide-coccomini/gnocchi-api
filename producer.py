#PRODUCER
import requests
import sys
import json
import subprocess
import re
import random
import threading
from datetime import datetime, timedelta

#sys.argv[1] = archive_policy_name

def get_token():
    global token
    global token_time
    p = subprocess.Popen('openstack token issue', shell=True, stdout=subprocess.PIPE)  
    output = p.communicate()[0]
    m = re.search('id(.+?)project_id', str(output))
    if m:
        token = m.group(1)[11:-5]
        token_time = datetime.now()

def list_metrics():
    global token
    url = 'http://252.3.27.148:8041/v1/metric'
    headers = {'X-Auth-Token':token}
    r = requests.get(url, headers=headers).json()
    for i in r:
        if i["archive_policy"]["name"] == sys.argv[1]:
            return i["id"]


def post_values():
    global token
    global token_time
    threading.Timer(5.0, post_values).start()
    if token == None or token_time < datetime.now() - timedelta(hours = 1):
    	get_token()

    id_metric = list_metrics()
    value = random.uniform(0.0,40.0)
    url = 'http://252.3.27.148:8041/v1/metric/'+str(id_metric)+'/measures'
    data = [{"timestamp":str(datetime.now()), "value":value}]
    print(sys.argv[1]+" measured: "+str(value))
    headers = {'Content-type': 'application/json', 'Content-Length':str(len(json.dumps(data))), 'X-Auth-Token':token}
    requests.post(url, data=json.dumps(data), headers=headers)

token = None
token_time = None

post_values()


