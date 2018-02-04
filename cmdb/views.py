from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
#import modules for crawler
import grab
import bs4
from bs4 import BeautifulSoup
# Create your views here.


def index(request):


    return render(request,"login.html");

def login(request):


    uname = request.POST.get("username")
    pwd = request.POST.get("password")

    g = grab.Grab(timeout=30,user_agent="Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)")
    g.go("https://login.uci.edu/ucinetid/webauth")
    g.doc.set_input('ucinetid', uname)
    g.doc.set_input('password', pwd)
    resp = g.doc.submit()

    mySoup = BeautifulSoup(resp.body, "html.parser")
    s = mySoup.find("div", {"id": "error-message"})
    try:
        return render(request,"login.html",{"data":[s.get_text()]})
    except:
        f = open("encript.txt", 'w')
        f.write(uname)
        f.write(",")
        f.write(pwd)
        f.close()
    return render(request, "search.html");









def searchUI(request):
    return render(request, "search.html");


def handleFormRequest(request):

    form_dict = dict()
    if request.method == "POST":
        print("Hello POOOOST")
        Breadth = request.POST.get("Breadth", None)
        Dept = request.POST.get("Dept", None)
        CourseNum = request.POST.get("CourseNum", None)
        CourseCodes = request.POST.get("CourseCodes", None)
        InstrName = request.POST.get("InstrName", None)
        Days = request.POST.get("Days", None)
        YearTerm = request.POST.get("YearTerm", None)
        ShowComments = request.POST.get("ShowComments", None)
        ShowFinals = request.POST.get("ShowFinals", None)
        CancelledCourses = request.POST.get("CancelledCourses", None)
        Bldg = request.POST.get("Bldg", None)
        Room = request.POST.get("Room", None)
        Division = request.POST.get("Division", None)
        CourseTitle = request.POST.get("CourseTitle", None)
        ClassType = request.POST.get("ClassType", None)
        StartTime = request.POST.get("StartTime", None)
        EndTime = request.POST.get("EndTime", None)
        MaxCap = request.POST.get("MaxCap", None)
        FullCourses = request.POST.get("FullCourses", None)
        Units = request.POST.get("Units", None)

        form_dict["Breadth"] = Breadth
        form_dict["Dept"] = Dept
        form_dict["CourseNum"] = CourseNum
        form_dict["CourseCodes"] = CourseCodes
        form_dict["InstrName"] = InstrName
        form_dict["Days"] = Days
        form_dict["YearTerm"] = YearTerm
        form_dict["ShowComments"] = ShowComments
        form_dict["ShowFinals"] = ShowFinals
        form_dict["CancelledCourses"] = CancelledCourses
        form_dict["Bldg"] = Bldg
        form_dict["Room"] = Room
        form_dict["Division"] = Division
        form_dict["CourseTitle"] = CourseTitle
        form_dict["ClassType"] = ClassType
        form_dict["StartTime"] = StartTime
        form_dict["EndTime"] =  EndTime
        form_dict["MaxCap"] = MaxCap
        form_dict["FullCourses"] = FullCourses
        form_dict["Units"] = Units
        print(form_dict)

        g = grab.Grab(timeout=30,
                      user_agent="Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)")
        g.go("https://www.reg.uci.edu/perl/WebSoc")

        for k in form_dict:
            if form_dict[k] != '':
                g.doc.set_input(k, form_dict[k])
        s = g.doc.submit()
        # submit user's query to reg.uci.edu

        text = s.body
        mySoup = BeautifulSoup(text, "html.parser")
        sbody = mySoup.body
        if_error = sbody.find('div', style="color: red; font-weight: bold;")
        ls = sbody.find('div', attrs={'class', 'course-list'})
        total_ls = []
        if if_error != None:
            result = {}
            result['error'] = sbody.find('div', style="color: red; font-weight: bold;").get_text()
            total_ls.append(result)
        else:
            table = list(ls.table)
            # big_class_ls = table.find_all('tr', bgcolor = "#fff0ff", valign = "top")
            #total_ls = []
            item_dict = {}
            find_big_class = 0
            index = 0
            item = 0
            while (index < len(table)):
                item = table[index]
                if find_big_class == 0:
                    if (type(item) == bs4.element.Tag and item.has_attr('bgcolor') and len(item) == 2):
                        bclass_name = str(list(item.td)[0]).replace('\xa0', '')
                        english_name = item.b.get_text()
                        item_dict["bclass"] = bclass_name
                        item_dict["name"] = english_name
                        item_dict["sclass"] = []
                        find_big_class = 1
                else:
                    if (type(item) == bs4.element.Tag and item.has_attr('valign') and len(item) == 16):
                        sclass_dict = {}
                        i = 0
                        key_ls = ["code", "type", "sec", "units", "instructor", "time", "place", "final", "max", "enr",
                                  "wl", "reg", "restr", "textbooks", "web", "status"]
                        for element in item:
                            sclass_dict[key_ls[i]] = element.get_text().replace("\xa0", " ")
                            i += 1
                        item_dict['sclass'].append(sclass_dict)
                    # len(item) == 1 and type(item) == bs4.element.Tag and item.has_attr('class') and item.has_attr('bgcolor')
                    if (type(item) == bs4.element.Tag and item.has_attr('bgcolor') and len(item) == 2):
                        total_ls.append(item_dict)
                        item_dict = {}
                        find_big_class = 0
                        index = index - 1
                index = index + 1
                if (index == len(table)):
                    total_ls.append(item_dict)

        response = JsonResponse(total_ls, safe=False)

        return render(request,"draggable.html",{"data":total_ls})


def modify_schedule(request):

    course_code = request.POST.get('course').split(",");
    print(course_code)

    to_return = [{"msg":"empty"}]
    g = grab.Grab(timeout=30,
                  user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")

    resp = g.go("https://www.reg.uci.edu/cgi-bin/webreg-redirect.sh")
    try:
        soup = BeautifulSoup(resp.body, "html.parser")
        redirect = soup.head.meta.attrs

        redirect = redirect[u'content'].strip("0;").strip().strip("url").strip("=")

    # redirect to login interface
        g.go(redirect)
    except:
        to_return = [{"msg":"school does not allow"},{"msg":"zhang yu shi ge sha bi"}]
        response = JsonResponse(to_return,safe=False)
        return response


    try:
        f = open("encript.txt", 'r')
        s = f.readline().split(",")
        uname = s[0]
        pwd = s[1]
    except:
        to_return = [{"msg":"File not found"}]

        # reutrn;
    g.doc.set_input("ucinetid", uname)
    g.doc.set_input("password", pwd)

    resp = g.doc.submit()
    # parse login result
    soup = BeautifulSoup(resp.body, "html.parser")
    redirect = soup.head.meta.attrs
    redirect = redirect[u'content'].strip("0;").strip().strip("url").strip("=")

    g.cookies.save_to_file("cookie.txt")
    g.setup(headers={
        'Cookie': '_ga=GA1.2.75746608.1516846905; ucinetid_auth=Pe1f1pi4DSkz8zUX52ClJcyzn5SH5J6KOYQFdYAHHL7FaSt5KVhjYFJbBrIx0F7E'})
    resp = g.go(redirect)  # log in webreg

    try:
        # go to enrollment window
        g.doc.choose_form(2)
        resp = g.doc.submit()
    except:
        to_return = [{"msg":"Your account is currently in use"}]
        print("Your account is currently in use, remember to log out next time!")


    try:
        # submit add course request

        to_return = []

        for c in range(len(course_code)-1):
            g.doc.set_input("courseCode", course_code[c])
            resp = g.doc.submit()
            soup = BeautifulSoup(resp.body, "html.parser")
            # print("\n\n seperation line\n\n")
            # print(soup.body)
            tag = soup.find("div", {"class": "WebRegErrorMsg"})
            print(tag.get_text())
            to_return.append({"msg":tag.get_text()})

    except:
        g.doc.choose_form(1)
        resp = g.doc.submit()
        # soup = BeautifulSoup(resp.body, "html.parser")
        # print(soup.body)

    # page:enrollmentMenu
    # mode:exit
    # call:0001
    # submit:Logout


    # after each operation logout
    g.doc.choose_form(1)
    resp = g.doc.submit()
    # soup = BeautifulSoup(resp.body,"html.parser")
    # print(soup.body)
    response = JsonResponse( to_return,safe=False)

    return response;

