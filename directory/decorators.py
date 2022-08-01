from basicLoginLogout.models import(
    APIkey
)
from rest_framework.parsers import JSONParser
from functools import wraps
from django.http.response import HttpResponse


def checkAuth(function):
    def wrapper(request):
        try:
            jsondata = JSONParser().parse(request)
            if len(APIkey.objects.filter(key=jsondata.get('key'))) == 1:
                return function(request)
        except Exception as e:
            return HttpResponse("some thin went wrong")
        return HttpResponse("do some thing")
    return wrapper