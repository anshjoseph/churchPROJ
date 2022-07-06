from re import A
from django.shortcuts import render, HttpResponse
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .modelSerializer import(
    SerialWard,
    SerialFamily,
    SerialPeople
)
from .models import(
    Ward,
    Family,
    People
)
from .requestSerializer import(
    AddFamily,
    AddPeople
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

# Create your views here.

def getpeople(request):
    data = SerialPeople(data=People.objects.all(),many=True)
    data.is_valid()
    return JsonResponse(data.data,safe=False)

@csrf_exempt
def makefamily(request):
    if request.method == "POST":
        data = AddFamily(data=JSONParser().parse(request))
        if data.is_valid():
            wardid = Ward.objects.get(id=data.data.get("wardid"))
            familyname = data.data.get('familyname')
            Family(wardid=wardid,familyname=familyname,membercount=0).save()        
            return HttpResponse(f"done")
        return HttpResponse("error")


@csrf_exempt
def makepeople(request):
    if request.method == "POST":
        data = AddPeople(data=JSONParser().parse(request))
        if data.is_valid():
            familyid = Family.objects.get(id=data.data.get("familyid"))
            name = data.data.get("name")
            age = data.data.get("age")
            People(familyid=familyid,name=name,age=age).save()
            return HttpResponse(f"done")
        return HttpResponse("error")
