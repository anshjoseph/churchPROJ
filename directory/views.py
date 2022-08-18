from tkinter.font import families
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Family, People, Ward
from django.utils import timezone
from .serializer import FamilySerializer, PeopleSerializer, WardSerializer
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters


def get_tokens_for_family(user):
    refresh = RefreshToken.for_user(user)
    return (
        str(refresh.access_token),
        str(refresh),
    )


class FamilySignupEndpoint(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:

            ward_id = request.data.get("ward_id", False)
            family_name = request.data.get("family_name", False)
            family_head_name = request.data.get("family_head_name", False)
            password = request.data.get("password", False)

            if not ward_id or not family_name or not family_head_name or not password:
                return Response(
                    {"error": "Missing Parameters"}, status=status.HTTP_400_BAD_REQUEST
                )

            if Family.objects.filter(
                ward_id=ward_id, family_head_name=family_head_name
            ).exists():
                return Response(
                    {"error": "Family Already Exists in this ward please login"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            family = Family(
                ward_id=ward_id,
                family_name=family_name,
                family_head_name=family_head_name,
            )

            family.save()

            family.set_password(password)
            family.last_login = timezone.now()

            family.save()

            serializer = FamilySerializer(family)

            access_token, refresh_token = get_tokens_for_family(family)
            return Response(
                {
                    "data": serializer.data,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong please try again later"})


class FamilySigninEndpoint(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:

            ward_id = request.data.get("ward_id", False)
            family_head_name = request.data.get("family_head_name", False)
            password = request.data.get("password", False)

            if not ward_id or not family_head_name or not password:
                return Response(
                    {"error": "Missing Parameters"}, status=status.HTTP_400_BAD_REQUEST
                )

            if not Family.objects.filter(
                ward_id=ward_id, family_head_name=family_head_name
            ).exists():
                return Response(
                    {"error": "Invalid Credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            family = Family.objects.get(
                ward_id=ward_id, family_head_name=family_head_name
            )

            if not family.check_password(password):
                return Response(
                    {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
                )

            family.last_login = timezone.now()

            family.save()

            access_token, refresh_token = get_tokens_for_family(family)

            serializer = FamilySerializer(family)

            return Response(
                {
                    "data": serializer.data,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong please try again later"})


class FamilyUpdateEndpoint(APIView):
    def put(self, request):

        family = Family.objects.get(pk=request.user.id)
        serializer = FamilySerializer(family, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid parameters passed"}, status=status.HTTP_400_BAD_REQUEST
        )


class FamilyMemberUpdateEndpoint(APIView):
    def put(self, request, pk=None):

        member = People.objects.get(family_id=request.user.id, pk=pk)
        serializer = PeopleSerializer(member, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid parameters passed"}, status=status.HTTP_400_BAD_REQUEST
        )


class WardListEndpoint(APIView):
    def get(self, request):
        try:
            wards = Ward.objects.all()
            serializer = WardSerializer(wards, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong please try again later"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChurchDirectoryEndpoint(APIView):

    filterset_fields = ("ward_id",)
    search_fields = (
        "^family_name",
        "^family_head_name",
    )

    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter,
    )

    def get(self, request):
        try:
            family = Family.objects.all()
            serializer = FamilySerializer(family, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong please try again later"},
                status=status.HTTP_200_OK,
            )


class FamilyMembersEndpoint(APIView):
    def get(self, request, pk=None):
        try:
            family = Family.objects.get(pk=pk)

            members = People.objects.filter(family=pk)

            family_data = FamilySerializer(family)
            member_data = PeopleSerializer(members, many=True)

            return Response(
                {"data": {"family": family_data.data, "members": member_data.data}},
                status=status.HTTP_200_OK,
            )

        except Family.DoesNotExist:
            return Response(
                {"error": "Requested Family does nopt exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong please try again later"},
                status=status.HTTP_400_BAD_REQUEST,
            )
