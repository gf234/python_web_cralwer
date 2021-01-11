from bs4 import BeautifulSoup
import requests

webpage = requests.get(
    "https://brand.naver.com/linefriends/category/453f0b424e1c4d7682fcf198687908fe?cp=1")
soup = BeautifulSoup(webpage.content, "html.parser")

for s in soup.find_all(attrs={'class': '_25CKxIKjAk'}):
    print(s)
