import grab
import bs4
from bs4 import BeautifulSoup
g = grab.Grab(timeout=30,user_agent="Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)")
g.go("https://www.reg.uci.edu/perl/WebSoc")

received_dict = {'Breadth': 'GE-4', 'Dept': ' ALL', 'CourseNum': '', 'CourseCodes': '',
                 'InstrName': '', 'Days': '', 'YearTerm': '2018-03', 'ShowComments': '',
                 'ShowFinals': '', 'CancelledCourses': 'Exclude', 'Bldg': '',
                 'Room': '', 'Division': 'ANY', 'CourseTitle': '',
                 'ClassType': 'ALL', 'StartTime': '',
                 'EndTime': '', 'MaxCap': '',
                 'FullCourses': 'ANY', 'Units': ''}


received_dict2 = {'Breadth': 'GE-2', 'Dept': ' ALL', 'CourseNum': '', 'CourseCodes': '',
                  'InstrName': 'Klef', 'Days': '', 'YearTerm': '2018-03', 'ShowComments': '',
                  'ShowFinals': '', 'CancelledCourses': 'Exclude', 'Bldg': '', 'Room': '',
                  'Division': 'ANY', 'CourseTitle': '', 'ClassType': 'ALL', 'StartTime': '',
                  'EndTime': '', 'MaxCap': '', 'FullCourses': 'ANY', 'Units': ''}
received_dict3 = {'Breadth': 'ANY', 'Dept': 'COMPSCI', 'CourseNum': '', 'CourseCodes': '',
                  'InstrName': '', 'Days': '', 'YearTerm': '2018-03', 'ShowComments': '',
                  'ShowFinals': '', 'CancelledCourses': 'Exclude', 'Bldg': '', 'Room': '',
                  'Division': 'ANY', 'CourseTitle': '', 'ClassType': 'ALL', 'StartTime': '',
                  'EndTime': '', 'MaxCap': '', 'FullCourses': 'ANY', 'Units': 'var'}

for k in received_dict3:
    if received_dict3[k] != '':
        g.doc.set_input(k,received_dict3[k])

# g.doc.set_input("YearTerm",input("YearTerm: (2018-03)"))
# g.doc.set_input("Breadth",input("Breadth: (ANY)"))
# g.doc.set_input("Dept",input("Dept: ( ALL)"))
# g.doc.set_input("CourseNum",input("CourseNum: ()"))
# g.doc.set_input("Division",input("Division: (ANY)"))
# g.doc.set_input("CourseCodes",input("CourseCodes: ()"))
# g.doc.set_input("InstrName",input("InstrName: ()"))
# g.doc.set_input("CourseTitle",input("CourseTitle: ()"))
# g.doc.set_input("ClassType",input("ClassType: (ALL)"))
# g.doc.set_input("Units",input("Units: ()"))
# g.doc.set_input("Days",input("Days: ()"))
# g.doc.set_input("StartTime",input("StartTime: ()"))
# g.doc.set_input("EndTime",input("EndTime: ()"))
# g.doc.set_input("MaxCap",input("Maxcap: ()"))
# g.doc.set_input("FullCourses",input("FullCourses: ()"))
# g.doc.set_input("FontSize",input("FontSize: (100)"))
# g.doc.set_input("CancelledCourses",input("CancelledCourses: (Exclude)"))
# g.doc.set_input("Bldg",input("Bldg: ()"))
# g.doc.set_input("Room",input("Room: ()"))

s = g.doc.submit()
text = s.body
mySoup = BeautifulSoup(text,"html.parser")
sbody = mySoup.body
if_error = sbody.find('div', style = "color: red; font-weight: bold;")
ls = sbody.find('div', attrs = {'class','course-list'})

if if_error != None:
    result = {}
    result['error'] = sbody.find('div', style = "color: red; font-weight: bold;").get_text()
    print(result)
else:
    table = list(ls.table)
    #big_class_ls = table.find_all('tr', bgcolor = "#fff0ff", valign = "top")
    total_ls = []
    item_dict = {}
    find_big_class = 0
    index = 0
    item = 0
    while(index < len(table)):
        item = table[index]
        if find_big_class == 0:
            if(type(item) == bs4.element.Tag and item.has_attr('bgcolor') and len(item) == 2):
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
                key_ls = ["code","type","sec","units","instructor","time","place", "final", "max","enr","wl","reg","restr","textbooks","web","status"]
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
        if(index == len(table)):
            total_ls.append(item_dict)

    # print(len(total_ls))
    for item in total_ls:
         print(len(item['sclass']))
         print(item)