import requests
import urllib

url = "Senator Cryin Chuck Schumer fought hard against the Bad Iran Deal even going at it with President Obama, & then Voted against it!"
url = urllib.parse.quote_plus(url)
url = "http://127.0.0.1:8000?claim=" + url
response = requests.get(url)

print(response.json())
