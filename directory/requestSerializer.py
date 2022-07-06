from rest_framework.serializers import Serializer
from rest_framework import serializers

class AddFamily(Serializer):
    wardid = serializers.IntegerField()
    familyname = serializers.CharField(max_length=300)

class AddPeople(Serializer):
    familyid = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
