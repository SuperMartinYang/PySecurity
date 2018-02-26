import requests

url = "http://www.baidu.com"
print requests.get(url).content
