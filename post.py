# -*- coding: UTF-8 -*-
import os
import urllib, urllib2

import re
import requests
import json
import datetime
import time

url = "http://202.4.153.28/FunctionPages/ReaderLog/SelectEnterOutLog.aspx"
headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
           'Connection': 'keep-alive',
           'Content-Length': '1436',
           'Host': '202.4.153.28',
           'Origin': 'http://202.4.153.28',
           'Referer': 'http://202.4.153.28/FunctionPages/ReaderLog/SelectEnterOutLog.aspx',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest',
           'Cookie': 'ASP.NET_SessionId=ar1e5pd2xoi0xcgnpgg3vc4u; yunsuo_session_verify=963975dae27279dcb717b852ff554518',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Cache-Control': 'no-cache'
           }
data = {'__EVENTTARGET': 'Form2$ctl01$btnSubmit',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '/wEPDwUINjIzNDg1NzRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYGBQVGb3JtMgUXRm9ybTIkY3RsMDAkZHBTdGFydERhdGUFFUZvcm0yJGN0bDAwJGRwRW5kRGF0ZQUaRm9ybTIkY3RsMDEkZGRsUmVhZGluZ1Jvb20FFUZvcm0yJGN0bDAxJGJ0blN1Ym1pdAUMRW50ZXJPdXRHcmlkRSnNrwoREEoyT+d/marzS8NG9tOpjy2O/8hnI4pl8J0=',
        '__VIEWSTATEGENERATOR': 'E938F432',
        'Form2$ctl00$dpStartDate': '2016-12-09',
        'Form2$ctl01$ddlReadingRoom': '',
        'Form2$ctl00$dpEndDate': '2016-12-09',
        'X_CHANGED': 'false',
        'X_TARGET': 'Form2_ctl01_btnSubmit',
        'Form2_Collapsed': 'false',
        'EnterOutGrid_Collapsed': 'false',
        'EnterOutGrid_SelectedRowIndexArray': '',
        'X_STATE': 'eyJGb3JtMl9jdGwwMF9kcFN0YXJ0RGF0ZSI6eyJUZXh0IjoiMjAxNi0xMC0wMiJ9LCJGb3JtMl9jdGwwMF9kcEVuZERhdGUiOnsiVGV4dCI6IjIwMTYtMTAtMDkifSwiRm9ybTJfY3RsMDFfZGRsUmVhZGluZ1Jvb20iOnsiRGF0YVRleHRGaWVsZCI6Ik5hbWUiLCJEYXRhVmFsdWVGaWVsZCI6Ik5vIiwiWF9JdGVtcyI6W1siIiwi5omA5pyJ6ZiF6KeI5a6kIiwxXSxbIjEwMTAwMSIsIuWMl+WMuuWbvuS5pummhuWbm+WxgumYheiniOWupCIsMV0sWyIxMDEwMDIiLCLljJfljLrlm77kuabppobkupTlsYLpmIXop4jlrqQiLDFdLFsiMjAxMDAxIiwi5LiA5bGC5oql5YiK6ZiF6KeI5Yy6IiwxXSxbIjIwMTAwMiIsIuS6jOWxguS4reaWh+enkeaKgOWbvuS5pumYheiniOWMuiIsMV0sWyIyMDEwMDMiLCLkuInlsYLnpL7np5Hlm77kuabpmIXop4jljLoiLDFdLFsiMjAxMDA0Iiwi5Zub5bGC5aSW5paH6ZiF6KeI5Yy6IiwxXSxbIjIwMTAwNSIsIuS6lOalvOaWh+eMrumYheiniOWMuiIsMV1dLCJTZWxlY3RlZFZhbHVlIjoiIn0sIkVudGVyT3V0R3JpZCI6eyJYX1Jvd3MiOnsiVmFsdWVzIjpbXSwiRGF0YUtleXMiOltdLCJTdGF0ZXMiOltdfX19',
        'X_AJAX': 'true'}
while True:
    seat = [-5] * 300
    seattime = [datetime.datetime.strptime('2015-04-07 19:11:21', '%Y-%m-%d %H:%M:%S')] * 300
    req = requests.post(url, data=data, headers=headers)
    response = req.text
    reg = r'"Values":(.*),"DataKeys"'
    userre = re.compile(reg)
    userlist = re.findall(userre, response)
    js = json.loads(userlist[0])
    for d in js:
        if d[0] == u'一层报刊阅览区':
            if seat[int(d[1])] == -5:
                seat[int(d[1])] = 0
            if d[2] == u'离开':
                seat[int(d[1])] += 1
            if d[2] == u'在座':
                seat[int(d[1])] -= 1
    for i in range(0, len(seat), 1):
        if seat[i] == 0:
            print(str(i) + u'离开\a'.encode('gbk'))

    for d in js:
        if d[0] == u'一层报刊阅览区':
            dtime = datetime.datetime.strptime("20" + d[3].encode('ascii'), '%Y-%m-%d %H:%M:%S')
            if dtime > seattime[int(d[1])]:
                seattime[int(d[1])] = dtime

    for i in range(0, len(seat), 1):
        if seat[i] != 0 and seat[i] != -5:
            devtime = datetime.datetime.now() - seattime[i]
            if devtime.days == 0 and devtime.seconds > 16100:
                print('%d  %s %d:%d \a' % (i, seattime[i].strftime('%Y-%m-%d %H:%M:%S'), (18000 - devtime.seconds) / 60,
                                           (18000 - devtime.seconds) % 60))
    print(u'结束'.encode('gbk'))
    time.sleep(300)
    os.system('cls')
