#coding:utf-8
import requests
import json
import csv
import random

baseurl = "https://mail.baidu.com" # 域名
cookie = "粘贴Cookie到此处"

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
filename = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba',5))+".csv"
with open(filename, 'w', newline='',encoding='utf-8-sig') as csvfile:
    fieldnames = ['总公司', '分公司','姓名','部门','邮箱','电话','地址']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    listurl = baseurl+"/coremail/s/json?sid="+cookiesid+"&func=oab%3AlistEx"
    for Director in res:
        for branch in Director['ou']:
            data = '{"dn":"'+Director['id']+'/'+branch['id']+'","returnAttrs":["@id","@type","department","true_name","email","gender","mobile_number","address"],"start":0,"limit":1000000000,"defaultReturnMeetingRoom":false}'
            branchperson = requests.post(listurl,data=data,headers=headers).json()['var']
            print(str(Director['name'])+" "+str(branch['name'])+" 共有人员 "+str(len(branchperson))+" 个")
            for person in branchperson:
                writer.writerow({'总公司':str(Director['name']),'分公司':str(branch['name']),'姓名':str(person['true_name']),'部门':str(person['department']),'邮箱':str(person['email']),'电话':str(person['mobile_number'])+" ",'地址':str(person['address'])})
                i+=1
print("共写入 "+str(i)+" 个联系人到文件 "+filename)
