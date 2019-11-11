import requests
import json

data = {'username':'adsfsdf', 'scores': '21654'}
data = json.dumps(data)
# data = 'zalupa'
headers = {'content_type': 'Application/json', 'scores': '21654'}
r = requests.post('http://localhost:9090/predict', data=data, headers=headers)
print(r.text)
