from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.


def login(request):


    return render(request,"login.html");


def searchUI(request):
    return render(request, "search.html");
