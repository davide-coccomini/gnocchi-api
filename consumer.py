#CONSUMER
import requests
import sys
import json
import subprocess
import re
import random
import threading
from datetime import datetime, timedelta

def get_token():
    global token
    global token_time
    p = subprocess.Popen('openstack token issue', shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0]
    m = re.search('id(.+?)project_id', str(output))
    if m:
        token = m.group(1)[11:-5]
        token_time = datetime.now()
        #print(token)

def list_metrics():
    global token
    url = 'http://252.3.27.148:8041/v1/metric'
    headers = {'X-Auth-Token':token}
    r = requests.get(url, headers=headers).json()
    if len(r) == 0:
        return None
    else:
        for i in r:
            if i["archive_policy"]["name"] == sys.argv[2]:
                id_metric = i["id"]
        return i["id"]

def get_metric(metric):
    global token
    threading.Timer(20.0, get_metric, [metric]).start()
    if token == None or token_time < datetime.now() - timedelta(hours = 1):
        get_token()
    id_metric = list_metrics()
    if id_metric != None:
        url = 'http://252.3.27.148:8041/v1/metric/'+str(id_metric)+'/measures?aggregation='+metric
        headers = {'X-Auth-Token':token}
        r = requests.get(url, headers=headers).json()
        if len(r) == 0:
            print("No measures inserted")
        else:
            print(sys.argv[1]+" "+sys.argv[2]+": "+str(r[0][2]))
    else:
        print("Metric not found")


token = None
token_time = None

metric = sys.argv[1]

get_metric(metric)


