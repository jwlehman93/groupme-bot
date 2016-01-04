import json
import urllib.request as req
import urllib.parse as par
import execjs
import os

runtime = execjs.get()
context = runtime.compile('''
    module.paths.push('%s');
    ng = require
                )
rugby_bot = execjs.eval('../bot')


def get_token(url):
    obj = [
        {
            "channel":"/meta/handshake",
            "version":"1.0",
            "supportedConnectionTypes":["long-polling"],
            "id":"1"
        }
    ]
    j_obj = json.dumps(obj)
    request = req.Request(url)
    request.add_header('Content-Type', 'application/json')
    response = req.urlopen(request, j_obj.encode('utf-8'))
    resp_obj = json.loads(response.read().decode('utf-8'))
    token = resp_obj[0]["clientId"]
    return token

get_token("https://push.groupme.com/faye")
