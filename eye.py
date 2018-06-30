# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
from bs4.element import Tag
import collections
import json


def getData(url):
    page = urllib.urlopen(url)
    html = BeautifulSoup(page, "lxml")
    div = html.find_all("div", attrs={"class": "col-sm-6", "id": "article-content"})
    dic = formatDiv(div[0])
    jsons = json.dumps(dic)
    print(jsons)


def formatDiv(div):
    dic = collections.OrderedDict()
    children = div.contents
    for child in children:
        if isinstance(child, Tag):
            if child.name != 'p' and child.name != 'ul' and child.name != 'table':
                text = collections.OrderedDict()
                count =1
                for sibling in child.next_siblings:
                    if isinstance(sibling, Tag):
                        if sibling.name == 'p':
                            text["text"+bytes(count)] = sibling.get_text()
                            count+=1
                        else:
                            if sibling.name == 'ul':
                                text["list"] = formatUl(sibling)
                            else:
                                break
                dic[child.get_text()] = text
            # if child.name =='ul'

    return dic


def formatUl(ul):
    dic = collections.OrderedDict()
    children = ul.contents
    count = 1
    for child in children:
        if isinstance(child, Tag) and child.name == 'li':
            text = child.get_text()
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


# def formatTanle()

# test = BeautifulSoup("<h1>Aphakic Glaucoma </h1>")
# getDict(test.h1)
dev = getData("http://webeye.ophth.uiowa.edu/eyeforum/cases/87-Myocilin-Juvenile-Open-Angle-Glaucoma.htm")

print(dev)
