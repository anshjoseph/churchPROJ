from re import A
from django.shortcuts import render, HttpResponse
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
import json
# sha256 for password
from hashlib import sha256

from basicLoginLogout.models import(
    APIkey
)
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
from basicLoginLogout.models import (
    LoginMaster,
    Session
    )
from .requestSerializer import(
    AddFamily,
    AddPeople,
    LoginFamily
)
from .responseSerializer import(
    Loginresponse,
    EndPointstatus,
    MakePeopleFamily,
    GetPeople
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .decorators import checkAuth
# Create your views here.

def getpeople(request):
    try:
        data = JSONParser().parse(request)
        if not len(APIkey.objects.filter(key=data.get('key'))) >= 1:
            return GetPeople(EndPointstatus.token_error,[]).response()
        if not len(Session.objects.filter(sessionid= data.get('sessionid'))) >= 1:
            return GetPeople(EndPointstatus.session_token_exp,[]).response()
        if len(APIkey.objects.filter(key=data.get('key'))) == 1:
            data = SerialPeople(data=People.objects.all(),many=True)
            data.is_valid()
            
            return GetPeople(EndPointstatus.success,list(data.data)).response()
        return GetPeople(EndPointstatus.json_not_valid,[]).response()
    except:
        return GetPeople(EndPointstatus.json_parse_error,[]).response()
    # return GetPeople(EndPointstatus.request_type_error,[]).response()

@csrf_exempt
def makefamily(request):
    if request.method == "POST":
        try:
            data=JSONParser().parse(request)
            
            if not len(APIkey.objects.filter(key=data.get('key'))) >= 1:
                return MakePeopleFamily(EndPointstatus.token_error).response()
            data = AddFamily(data=data)
            if data.is_valid():
                wardid = Ward.objects.get(id=data.data.get("wardid"))
                familyname = data.data.get('familyname')
                phoneno = data.data.get('phoneno')
                password = data.data.get("password")
                family = Family(wardid=wardid,familyname=familyname,phoneno=phoneno,membercount=0)
                family.save()
                LoginMaster(family=family,password=password).save()
                return MakePeopleFamily(EndPointstatus.success).response()
            return MakePeopleFamily(EndPointstatus.json_not_valid).response()
        except Exception as e:
            return MakePeopleFamily(EndPointstatus.json_parse_error).response()
    return MakePeopleFamily(EndPointstatus.request_type_error).response()

@csrf_exempt
def loginfamily(request):
    if request.method == "POST":
        try:
            data=JSONParser().parse(request)
            if not len(APIkey.objects.filter(key=data.get('key'))) >= 1:
                return Loginresponse(EndPointstatus.token_error).response()
            data = LoginFamily(data=data)
            if data.is_valid():
                phoneno = data.data.get("phoneno")
                password = sha256(str(data.data.get("password")).encode('utf-8')).hexdigest()
                family = list(Family.objects.filter(phoneno=phoneno))[0]
                loginsession = LoginMaster.objects.get(family=family)
                if str(loginsession.passwordhash) == password:
                    session = Session(familyid=loginsession)
                    session.save()
                    sessionid = str(session.sessionid)
                    return Loginresponse(EndPointstatus.success,sessionid).response()
                return Loginresponse(EndPointstatus.auth_problem,"").response()
            return Loginresponse(EndPointstatus.json_not_valid,"").response()
        except Exception as e:
            print(e)
            return Loginresponse(EndPointstatus.json_parse_error,"").response()
    return Loginresponse(EndPointstatus.request_type_error,"").response()

@csrf_exempt
def makepeople(request):
    if request.method == "POST":
        try:
            data=JSONParser().parse(request)
        
            if not len(APIkey.objects.filter(key=data.get('key'))) >= 1:
                return MakePeopleFamily(EndPointstatus.token_error).response()
            if not len(Session.objects.filter(sessionid= data.get('sessionid'))) >= 1:
                return MakePeopleFamily(EndPointstatus.session_token_exp).response()
            data = AddPeople(data=data)
            if data.is_valid():
                familyid = Family.objects.get(id=data.data.get("familyid"))
                name = data.data.get("name")
                age = data.data.get("age")
                People(familyid=familyid,name=name,age=age).save()
                return MakePeopleFamily(EndPointstatus.success).response()
            return MakePeopleFamily(EndPointstatus.json_not_valid)
        except:
            return MakePeopleFamily(EndPointstatus.json_parse_error).response()
    return MakePeopleFamily(EndPointstatus.request_type_error).response()


