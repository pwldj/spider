# coding=utf-8
import urllib
import re
from urllib import quote


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


def getUser(html):
    reg = r'key=tblog_search_user&value=user_feed_1_num\\">([0-9]*)'
    userre = re.compile(reg)
    userlist = re.findall(userre, html)
    return userlist


name = "帕瓦罗蒂金"
html = getHtml("http://s.weibo.com/user/" + quote(quote(name)) + "&Refer=weibo_user")

print(getUser(html))
