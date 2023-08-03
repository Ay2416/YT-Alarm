import re
import requests
from bs4 import BeautifulSoup

url = 'your_youtube_link'
res = requests.get(url)

soup = BeautifulSoup(res.text, "html.parser")

elems = soup.find_all(itemprop=re.compile("identifier"))

print(elems[0].attrs['content'])
