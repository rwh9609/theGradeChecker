import smtplib
import re
from robobrowser import RoboBrowser
import hashlib
import sys
import time

# creates a browser object
browser = RoboBrowser(history=True)

# opens the page to be scraped
browser.open('')

# creates a form object
form = browser.get_form()

# writes to the forms named 'UserName' and 'Password' the values passed to it
form['UserName'].value = 'user'
form['Password'].value = 'pass'

# added in some timers so as to not overload the web server
time.sleep(3)

# clicks the submit button
browser.submit_form(form)
time.sleep(3)

# opens the page which has the grades
browser.open('')

# creates a hash object
m = hashlib.md5()

# produces a hash of the browser content
m.update(browser.response.content)

# if a hash already exists, then read a line
# if it doesn't, then create a new hash
try:
    checkhash = open('','r')
    checkhash = checkhash.readline()
except:
    file = open('','w')
    newhash = m.hexdigest()
    file.write(newhash)
    print 'Writing the hash for the first time'
    checkhash = m.hexdigest()

# if the saved hash isn't the same as the new hash
# then something on the page has been altered; in the case, a grade has been updated
if m.hexdigest() != checkhash:
    content = 'grade has changed'

    # uses the SMTP to send an email to alert that a grade has been changed
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('user', 'password')
    mail.sendmail('','',content)
    mail.close()
    file = open('','w')
    newhash = m.hexdigest()
    file.write(newhash)
    sys.exit()
else:
    print m.hexdigest()
    print checkhash
    file = open('','w')
    uphash = m.hexdigest()
    file.write(uphash)
    sys.exit()
