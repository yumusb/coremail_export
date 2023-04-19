#coding:utf-8
import requests
import json
import csv
import random
import time


def getcompany(Director,branch):
    global companys
    companys[Director['id']+'/'+branch['id']]=Director['name']+"*"+branch['name']
    if 'ou' in branch.keys():
        for branch1 in branch['ou']:
            getcompany(Director,branch1)
baseurl = "https://mail.baidu.com" # 域名
cookie = "粘贴cookie到这里"

try:
    cookiesid = cookie.split("Coremail.sid=")[1].split(";")[0] # cookie或者url中去找到的
    cookieCoremail = cookie.split("Coremail=")[1].split(";")[0] # cookie中的Coremail字段
except:
    print("Cookie有问题?请检查")
    exit()
print("cookiesid:"+cookiesid+",Coremail:"+cookieCoremail)

headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Accept": "text/x-json",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type": "text/x-json",
        "X-Requested-With": "XMLHttpRequest",
        "referrer": baseurl+"/coremail/XT5/index.jsp?sid="+cookiesid,
        "Cookie": "face=auto; locale=zh_CN; Coremail="+cookieCoremail+";Coremail.sid="+cookiesid
    }
getDirectoriesurl = baseurl+"/coremail/s/json?sid="+cookiesid+"&func=oab%3AgetDirectories"

body = "{\"attrIds\":[\"email\"]}"
res = requests.post(getDirectoriesurl,data=body,headers=headers).json()['var']
companys = {}
for Director in res:  ## 多级子公司
    for branch in Director['ou']:
        getcompany(Director,branch)
print("共获取到子公司 "+str(len(companys))+" 个\n开始获取字段信息")
getattrsUrl = baseurl + "/coremail/XT5/index.jsp?sid="+cookiesid
attrsHtml = requests.get(getattrsUrl,headers=headers).text
attrStr = attrsHtml.split("'returnattrs':")[1].split("],")[0]
attrList = [s.strip().strip("'") for s in attrStr[1:-1].split(',')]
print(attrList)
i=0
b=0
fieldnames = attrList
fieldnames.insert(0,"分公司")
fieldnames.insert(0,"总公司")
filename = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba',5))+".csv"
listurl = baseurl+"/coremail/s/json?sid="+cookiesid+"&func=oab%3AlistEx"
with open(filename, 'w', newline='',encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for company in companys:
        data = '{"dn":"'+company+'","returnAttrs":'+attrStr+'],"start":0,"limit":1000000000,"defaultReturnMeetingRoom":false}'
        branchperson = requests.post(listurl,data=data,headers=headers).json()['var']
        print(companys[company]+" 共有人员 "+str(len(branchperson))+" 个")
        Dname,Bname = companys[company].split("*")
        for person in branchperson:
            person['总公司'] = str(Dname)
            person['分公司'] = str(Bname)
            writer.writerow(person)
            i+=1
        b+=1
        if b%7==0: ##每获取几个子公司后进行sleep 防止IP被ban掉，可以自定修改
            time.sleep(2)
print("共写入 "+str(i)+" 个联系人到文件 "+filename)
