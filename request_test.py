import requests

req = requests.Session()
url = 'http://127.0.0.1:8080/api/login/'
b_url = 'http://127.0.0.1:8000/login/'
res = req.get(url)
print(res.text)
#3b_res = req.get(b_url)
#3print(b_res.text)
