import re
import requests
from bs4 import BeautifulSoup

url = 'your_youtube_link'
res = requests.get(url)

soup = BeautifulSoup(res.text, "html.parser")

elems1 = soup.find_all(rel=re.compile("image_src"))

print(elems1[0].attrs["href"])
