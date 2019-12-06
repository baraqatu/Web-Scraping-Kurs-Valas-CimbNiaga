# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 19:25:11 2019

@author: Abazmu
"""

# syntax for scrapping website
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.cimbniaga.co.id/id/personal/index"
html = urlopen(url)
type(html)
soup = BeautifulSoup(html, 'lxml')
datas = soup.find_all('tr')
len(datas)
txts = []
for row in datas:
    text = list(row.stripped_strings)
    txts.append(text)

colCountry = []
colBuy = []
colSell = []

for index in range(0, 15):
    colCountry.append(txts[index][0])
    colBuy.append(txts[index][1])
    colSell.append(txts[index][2])


# import Tabel to Website
from flask import Flask, Blueprint, render_template
from werkzeug.contrib.fixers import ProxyFix

web_app = Blueprint('app', __name__)
@web_app.route('/')
def hello():
    return render_template('index.html', country=colCountry, buy=colBuy, sell=colSell)

if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(web_app, url_prefix='/')

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
