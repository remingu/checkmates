#!/usr/bin/env python3
import requests
import json
 
 
 
def login() -> str:
    logincreds = {'user': 'dashboardadmin',
                   'password': 'yourpwd'}
    header = {'Content-type': 'application/json'}
    logincreds = json.dumps(logincreds)
    print(logincreds)
    req = requests.post('https://192.168.0.1/web_api/login', data=logincreds, verify=False, headers=header)
    print(req.content)
    req = json.loads(req.content)
    sid = (req['sid'])
    return sid
 
def add_host(sid: str, hostname: str, ipv4address: str) :
    header = {'Content-type': 'application/json', 'X-chkp-sid': sid}
    payload = {
        'name': hostname,
        'ipv4-address': ipv4address
    }
    payload = json.dumps(payload)
    req = requests.post('https://192.168.0.1/web_api/add-host', data=payload, verify=False, headers=header)
    req = req.content
    return req
 
def publish(sid: str):
    header = {'Content-type': 'application/json', 'X-chkp-sid': sid}
    payload = {}
    payload = json.dumps(payload)
    req = requests.post('https://192.168.0.1/web_api/publish', data=payload, verify=False, headers=header)
    req = req.content
    return req
 
def logout(sid: str):
    header = {'Content-type': 'application/json', 'X-chkp-sid': sid}
    payload = {}
    payload = json.dumps(payload)
    req = requests.post('https://192.168.0.1/web_api/logout', data=payload, verify=False, headers=header)
    req = req.content
    return req
 
 
 
 
if __name__ == '__main__':
    sid = login()
    add_host(sid, 'host1', '192.168.10.2')
    publish(sid)
    logout(sid)
