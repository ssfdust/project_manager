from django.test import TestCase
import requests

# Create your tests here.
req = requests.Session()
s = req.get('http://127.0.0.1:8000/login')
print(s.cookies)
