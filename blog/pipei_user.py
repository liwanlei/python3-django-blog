# -*- coding:utf-8 -*-  
import re
import sys
def getPhoneNumFromFile(fobj):#手机号
    regex = re.compile(r'1\d{10}', re.IGNORECASE)
    phonenums = re.findall(regex, fobj)
    return phonenums
def getMailAddFromFile(fobj):#email
    regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)
    mails = re.findall(regex, fobj)
    return mails
def getuser(fobj):#验证用户名、密码
    regex = re.compile(r"^[a-zA-Z]\w{5,15}$", re.IGNORECASE)
    user = regex.findall(fobj)
    return user
def getqq(fobj):#qq
    regex = re.compile(r"[1-9][0-9]{4,11}", re.IGNORECASE)
    user = regex.findall(fobj)
    return user
# if __name__ == '__main__':
#     he=getMailAddFromFile('1596463619@163.com')
#     print(he)
#     print(getuser('idfpoijojojijdsfdsij'))
#     print(getqq('95295'))
