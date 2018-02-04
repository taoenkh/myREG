from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.


def login(request):


    return render(request,"login.html");


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
    return HttpResponse("Hello World")