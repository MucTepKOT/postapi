import requests
import json

data = {'username':'adsfsdf', 'scores': {'21654':'fgdgfdg'}}
print(len(data))
data = json.dumps(data)
r = requests.post('http://localhost:9090/predict', data=data)
print(r.text)
