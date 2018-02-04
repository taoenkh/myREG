import grab
import re
from bs4 import BeautifulSoup



g = grab.Grab(timeout=30,user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")

resp = g.go("https://www.reg.uci.edu/cgi-bin/webreg-redirect.sh")

soup = BeautifulSoup(resp.body,"html.parser")
redirect = soup.head.meta.attrs


redirect = redirect[u'content'].strip("0;").strip().strip("url").strip("=")

#redirect to login interface

g.go(redirect)


try:
    f = open("encript.txt",'r')
    s = f.readline().split(",")
    uname = s[0]
    pwd = s[1]
except:
    print("file not found")
    #reutrn;
g.doc.set_input("ucinetid",uname)
g.doc.set_input("password",pwd)



resp = g.doc.submit()
# parse login result
soup = BeautifulSoup(resp.body,"html.parser")
redirect = soup.head.meta.attrs
redirect = redirect[u'content'].strip("0;").strip().strip("url").strip("=")


g.cookies.save_to_file("cookie.txt")
g.setup(headers={'Cookie': '_ga=GA1.2.75746608.1516846905; ucinetid_auth=Pe1f1pi4DSkz8zUX52ClJcyzn5SH5J6KOYQFdYAHHL7FaSt5KVhjYFJbBrIx0F7E'})
resp = g.go(redirect) # log in webreg


try:
# go to enrollment window
    g.doc.choose_form(2)
    resp = g.doc.submit()
except:
    print("Your account is currently in use, remember to log out next time!")

try:
#submit add course request
    g.doc.set_input("courseCode","98765")
    resp = g.doc.submit()
    soup = BeautifulSoup(resp.body,"html.parser")
    # print("\n\n seperation line\n\n")
    # print(soup.body)
    tag = soup.find("div",{"class":"WebRegErrorMsg"})
    print(tag.get_text())
except:
    g.doc.choose_form(1)
    resp = g.doc.submit()
    # soup = BeautifulSoup(resp.body, "html.parser")
    # print(soup.body)

# page:enrollmentMenu
# mode:exit
# call:0001
# submit:Logout


#after each operation logout
g.doc.choose_form(1)
resp = g.doc.submit()
# soup = BeautifulSoup(resp.body,"html.parser")
# print(soup.body)