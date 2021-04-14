#coding:utf-8
import requests 

import json

baseurl = "https://email.coremail.com.cn"

cookiesid = "123" # cookie去找
cookieCoremail = "456"

getDirectoriesurl = baseurl+"/coremail/s/json?sid="+cookiesid+"&func=oab%3AgetDirectories"

headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Accept": "text/x-json",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type": "text/x-json",
        "X-Requested-With": "XMLHttpRequest",
        "referrer": baseurl+"/coremail/XT5/index.jsp?sid="+cookiesid,
        "Cookie": "face=auto; locale=zh_CN; Coremail="+cookieCoremail+";Coremail.sid="+cookiesid
    }
body = "{\"attrIds\":[\"email\"]}"

res = requests.post(getDirectoriesurl,data=body,headers=headers).json()['var']

listurl = baseurl+"/coremail/s/json?sid="+cookiesid+"&func=oab%3AlistEx"
for Director in res:
    for bumen in Director['ou']:
        data = '{"dn":"'+Director['id']+'/'+bumen['id']+'","returnAttrs":["@id","@type","true_name","email","gender"],"start":0,"limit":1000000000,"defaultReturnMeetingRoom":false}'
        for person in requests.post(listurl,data=data,headers=headers).json()['var']:
            print(Director['name']+","+bumen['name']+","+person['true_name']+","+person['email'])