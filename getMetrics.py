#GET METRIC AVAILABLE
import requests
import sys
import json
import subprocess
import re

def get_token():
    global token
    global token_time
    p = subprocess.Popen('openstack token issue', shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0]
    m = re.search('id(.+?)project_id', str(output))
    if m:
        token = m.group(1)[11:-5]

def list_metrics():
    global token
    url = 'http://252.3.27.148:8041/v1/metric'
    if token == None:
        get_token()
    headers = {'X-Auth-Token':token}
    r = requests.get(url, headers=headers).json()
    if len(r) == 0:
        print("No metrics available")
    else:
        index = 1
        print("Metrics available: ")
        for i in r:
            print(str(index)+") "+i["archive_policy"]["name"])
            index += 1

token = None

list_metrics()
