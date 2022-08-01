from rest_framework.serializers import ModelSerializer
from .models import Ward,Family,People


# WARD SERIALIZER
class SerialWard(ModelSerializer):
    class Meta:
        model = Ward
        fields = ["id","wardname","wardhead"]


# FAMILY SERIALIZER
class SerialFamily(ModelSerializer):
    class Meta:
        model = Family
        fields = ["id","familyname","membercount"]


# PEOPLE SERIALIZER
class SerialPeople(ModelSerializer):
    class Meta:
        model = People
        fields = ["id","familyid","name","age"]
