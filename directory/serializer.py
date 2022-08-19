from dataclasses import field
from rest_framework import serializers
from .models import Family, People, Ward


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = "__all__"

        # These fields are displayed but not editable and have to be a part of 'fields' tuple
        read_only_fields = (
            "is_admin",
            "is_staff",
            "is_superuser",
        )

        # These fields are only editable (not displayed) and have to be a part of 'fields' tuple
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = "__all__"


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = "__all__"
