from bs4 import BeautifulSoup
import pandas as pd
from pandas import Series, DataFrame
from sqlalchemy import create_engine
import requests
import re
import pymysql

# db 설정
pymysql.install_as_MySQLdb()

# 사이트 소스 가져오기 현재는 특정 카테고리 지정
webpage = requests.get(
    "https://brand.naver.com/linefriends/category/453f0b424e1c4d7682fcf198687908fe?cp=1")
soup = BeautifulSoup(webpage.content, "html.parser")

raw_data = {'img': [], 'name': [], 'price': [], 'category': [],
            'detail': [], 'created': [], 'modified': []}
# 상품 정보 뽑아내기
for s in soup.find_all(attrs={'class': '-qHwcFXhj0'}):
    imgTag = s.find('img')
    img = imgTag['src']
    name = imgTag['alt']
    price = int(s.find('span', class_='nIAdxeTzhx').string.replace(',', ''))
    raw_data['img'].append(img)
    raw_data['name'].append(name)
    raw_data['price'].append(price)
    raw_data['category'].append('토이')
    raw_data['detail'].append('상세 정보')
    raw_data['created'].append(pd.datetime.now())
    raw_data['modified'].append(pd.datetime.now())

df = DataFrame(raw_data)

with open('db.txt', 'r') as f:
    user = f.readline().replace('user=', '', 1).rstrip()
    password = f.readline().replace('password=', '', 1).rstrip()

    engine = create_engine('mysql://'+user+':'+password +
                           '@localhost/linestore', encoding='utf-8')
    df.to_sql('product', engine, if_exists='replace', index=False)
