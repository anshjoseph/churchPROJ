from abc import abstractmethod
from sre_constants import SUCCESS
from django.shortcuts import HttpResponse
import json

"""
        0: succes
        1: token error
        2: auth problem
        3: json parse error
        4: request type error
"""
class EndPointstatus(object):
    success:int = 0
    token_error:int = 1
    auth_problem:int  = 3
    json_parse_error:int = 4
    request_type_error:int = 5 
    json_not_valid:int = 6
    entry_completed:int = 7
    session_token_exp = 8 

class JSONresponse(object):
    def __init__(self) -> None:
        self.contentType = 'appliction/json'
    @abstractmethod
    def response(self)->HttpResponse:
        pass
class Loginresponse(JSONresponse):
    def __init__(self,errorCode:int,sessionid) -> None:
       
        super().__init__()
        self.data = {
            "code":errorCode,
            "sessionid":sessionid
        }
    def response(self) -> HttpResponse:
        return HttpResponse(json.dumps(self.data),content_type=self.contentType)
class MakePeopleFamily(JSONresponse):
    def __init__(self,errorCode:int) -> None:
        super().__init__()
        self.data = {
            "code":errorCode
        }
    def response(self) -> HttpResponse:
        return HttpResponse(json.dumps(self.data),content_type=self.contentType)
class GetPeople(JSONresponse):
    def __init__(self,errorCode:int,data) -> None:
        super().__init__()
        self.data = {
            "code":errorCode,
            "data": data
        }
    def response(self) -> HttpResponse:
        return HttpResponse(json.dumps(self.data),content_type=self.contentType)
