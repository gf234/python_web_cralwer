from bs4 import BeautifulSoup
import pandas as pd
from pandas import Series, DataFrame
import requests
import re
import pymysql

# 사이트 소스 가져오기
webpage = requests.get(
    "https://brand.naver.com/linefriends/category/453f0b424e1c4d7682fcf198687908fe?cp=1")
soup = BeautifulSoup(webpage.content, "html.parser")

raw_data = {'img': [], 'name': [], 'price': [], 'category': [], 'detail': []}
# 상품 정보 뽑아내기
for s in soup.find_all(attrs={'class': '-qHwcFXhj0'}):
    imgTag = s.find('img')
    img = imgTag['src']
    name = imgTag['alt']
    price = s.find('span', class_='nIAdxeTzhx').string.replace(',', '')
    raw_data['img'].append(img)
    raw_data['name'].append(name)
    raw_data['price'].append(price)
    raw_data['category'].append('토이')
    raw_data['detail'].append('상세 정보')

df = DataFrame(raw_data)

db = pymysql.connect()
