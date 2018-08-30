import smtplib
import re
from robobrowser import RoboBrowser
import hashlib
import sys
import time
browser = RoboBrowser(history=True)
browser.open('https://selfservice.utulsa.edu/Student/Account/Login?ReturnUrl=%2fstudent')
form = browser.get_form()
form['UserName'].value = 'user'
form['Password'].value = 'pass'
time.sleep(3)
browser.submit_form(form)
time.sleep(3)
browser.open('https://selfservice.utulsa.edu/Student/Student/Grades/GetStudentGradeInformationAsync')
m = hashlib.md5()
m.update(browser.response.content)
try:
    checkhash = open('/Users/Documents/hash.txt','r')
    checkhash = checkhash.readline()
except:
    file = open('/Users/Documents/hash.txt','w')
    newhash = m.hexdigest()
    file.write(newhash)
    print 'Writing the hash for the first time'
    checkhash = m.hexdigest()
if m.hexdigest() != checkhash:
    content = 'grade has changed'
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('user', 'password')
    mail.sendmail('tophatmcbabs@gmail.com','tophatmcbabs@gmail.com',content)
    mail.close()
    file = open('/Users/Documents/hash.txt','w')
    newhash = m.hexdigest()
    file.write(newhash)
    sys.exit()
else:
    print m.hexdigest()
    print checkhash
    file = open('/Users/Documents/hash.txt','w')
    uphash = m.hexdigest()
    file.write(uphash)
    sys.exit()
