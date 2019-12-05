# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 19:25:11 2019

@author: Abazmu
"""

import pandas as pd

#%matplotlib inline

# syntax for scrapping website
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.cimbniaga.co.id/id/personal/index"
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')
type(soup)

title = soup.title
text = soup.get_text()
#print(soup.text)

#soup.find_all('a')
#all_links = soup.find_all("a")
#for link in all_links:
#    print(link.get("href"))

rows = soup.find_all('tr')
#print(rows[:10])

for row in rows:
    row_td = row.find_all('td')
#print(row_td)
type(row_td)

str_cells = str(row_td)
cleantext = BeautifulSoup(str_cells, "lxml").get_text()
#print(cleantext)

import re
list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '', str_cells))
    list_rows.append(clean2)
#print(clean2)
type(clean2)


# Mengubah data frame dan menampilkan dengan 10 baris pertama
# Menggunakan Library Pandas (Berfungsi untuk merapikan dataframe)
df = pd.DataFrame(list_rows)
df.head(10)

# Membagi kolom 0 menjadi beberapa kolom agar terlihat rapi
# dengan mengggunakan method str.split()
df1 = df[0].str.split(',', expand=True)
df1.head(10)

# Menghapus kurung siku pada setiap barus
# dengan menggunakan method str.strip() untuk menghapus brecket pada kolom 0
df1[0] = df1[0].str.strip('[')
df1[2] = df1[2].str.strip(']')
df1.head(10)

col_labels = soup.find_all('th')
all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)

df2 = pd.DataFrame(all_header)
df2.head()

df3 = df2[0].str.split(',', expand=True)
df3.head()

frames = [df3, df1]
df4 = pd.concat(frames)
df4.head(10)

df5 = df4.rename(columns=df4.iloc[0])
df5.head()

df5.info()
df5.shape

df5 = df4.dropna(axis=0, how='any', thresh=None, subset=None)

df6 = df5.drop(df5.index[0])


# Membuat Bar Chart menggunakan method matplotlib
import matplotlib.pyplot as plt
import numpy as np





# import Tabel to Website
from flask import Flask, Blueprint, render_template
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

web_app = Blueprint('cimb.py', __name__)
@web_app.route('/')
def index():
    return render_template('index.html', data=df6)
if __name__ == '__main__':
    exampleScrapping = Flask(__name__)
    exampleScrapping.register_blueprint(web_app, url_prefix='/')
    exampleScrapping.wsgi_app = ProxyFix(exampleScrapping.wsgi_app)
    exampleScrapping.run()
