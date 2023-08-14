from urllib.request import Request, urlopen
import urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input("Enter - ")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
req = Request(url, headers=headers)
html = urlopen(req, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# Retrieve all of the anchor tags
tags = soup("a")
url_pattern = re.compile(r"https?://\S+|www\.\S+")
for tag in tags:
    hrefData = tag.get("href", None)
    if hrefData and url_pattern.match(hrefData):
        print(hrefData)
