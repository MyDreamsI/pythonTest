# encoding:utf-8
import urllib.request

from bs4 import BeautifulSoup

import pymysql

url = "https://movie.douban.com/top250"

movelist = []

def get_html(url):
    #获取url上的内容
    res = urllib.request.urlopen(url)
    #解码
    html = res.read().decode()

    return  html


def parse_html(htmlfile):
    #解析html页面
    mysoup = BeautifulSoup(htmlfile,'html.parser')

    movie_zone = mysoup.find('ol')

    move_list =movie_zone.find_all('li')

    for movie in move_list:

        movie_name = movie.find('span',attrs = {'class':'title'}).getText()

        movelist.append(movie_name)

    nextpage = mysoup.find('span',attrs = {'class':'next'}).find('a')
    if nextpage:
        new_url = url+nextpage['href']
        parse_html(get_html(new_url))
    return movelist

#存储到数据库
def save_data(movelist):
    conn = pymysql.connect(host = 'localhost',user = 'root',password = 'root',db = 'test')

    mycursor = conn.cursor()

    for move in movelist:
        sql="insert into name (name) values (%s)"
        mycursor.execute(sql,move)
    conn.commit()
    mycursor.close()
    conn.close()
    #pass

reshtml = get_html(url)
reshtml = parse_html(reshtml)
save_data(reshtml)








