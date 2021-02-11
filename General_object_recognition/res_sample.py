# encoding:utf-8

import requests
import base64
import json

filename = 'res.json'
request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
f = open('./res.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image": img}
access_token = 'your own access_token'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    with open(filename, 'w', encoding='utf-8') as file_obj:
        json.dump(response.json(), file_obj, ensure_ascii=False, indent=4)
reslines = response.json()['result']
res = ' '.join(lines['keyword'] for lines in reslines)
print(res)
