# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import print_function
import os
import re
import shutil
import time
import urllib
from bs4 import BeautifulSoup
from bs4.element import Tag
import collections
import json
import socket


def getData(url, st):
    path = 'D:/eye/' + re.sub("[:\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),
                              st).replace(' ', '_') + '/'
    isExists = os.path.exists(path[:-1] + "_/")
    if not isExists:
        if not os.path.exists(path):
            os.makedirs(path)
            print(path + u' 创建成功')
        page = urllib.urlopen(url)
        html = BeautifulSoup(page, "lxml")
        div = html.find_all("div", attrs={"class": "col-sm-6", "id": "article-content"})
        dic = formatDiv(div[0], url)
        jsons = json.dumps(dic, indent=4)
        with open(path + 'text.txt', "w") as f:
            f.write(jsons)
        getimg(div[0], path)
        print(path)
        shutil.move(path, path[:-1] + "_/")
        time.sleep(3)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + u' 目录已存在')


def getimg(div, path):
    imgurl = div.find_all("a")
    count = 0
    for url in imgurl:
        if url['href'] != '':
            if url['href'].split('.')[-1] == 'jpg' or url['href'].split('.')[-1] == 'png' or url['href'].split('.')[
                -1] == 'jpeg':
                urllib.urlretrieve('http://webeye.ophth.uiowa.edu/eyeforum' + url['href'][2:],
                                   path + '/' + bytes(count) + '.' + url['href'].split('.')[-1])
                count += 1
                time.sleep(2)


def formatUl(ul):
    dic = collections.OrderedDict()
    children = ul.contents
    count = 1
    for child in children:
        if isinstance(child, Tag) and child.name == 'li':
            text = child.get_text(strip=True)
            flag = 0
            for nextli in child.next_siblings:
                if isinstance(child, Tag) and nextli.name == 'ul':
                    dic[text] = formatUl(nextli)
                    flag = 1
                    break
            if flag == 0:
                if text.find(':') == -1:
                    dic["text" + bytes(count)] = text
                    count += 1
                else:
                    dic[text.split(':')[0]] = text.split(':')[1]
    return dic


def formatDiv(div, url):
    children = div.contents
    data = []
    dic = collections.OrderedDict()
    beginner = 0
    flag = 0

    for i in range(len(children)):
        if isinstance(children[i], Tag):
            data.append(children[i])
            if flag == 0 and children[i].get_text().find('Chief Complaint') == -1:
                beginner += 1
            else:
                flag = 1
    dic['title'] = data[0].get_text(strip=True) + '|' + data[1].get_text(strip=True)
    dic['url'] = url
    for i in range(beginner, len(data)):
        if data[i].name == "ul":
            dic[bytes(i)] = formatUl(data[i])
        else:
            text = data[i].get_text(strip=True)
            if text.find(':') == -1:
                dic[bytes(i)] = text
            else:
                dic[bytes(i)] = {text.split(':')[0]: text.split(':')[1]}
    return dic


def geturl(url):
    page = urllib.urlopen(url)
    html = BeautifulSoup(page, "lxml")
    div = html.find_all("div", attrs={"class": "container-fluid"})
    urls = div[3].find_all("p")
    for url in urls:
        if url.find('a'):
            getData("http://webeye.ophth.uiowa.edu/eyeforum/" + url.a['href'], url.a.string)


dev = geturl("http://webeye.ophth.uiowa.edu/eyeforum/cases.htm")
