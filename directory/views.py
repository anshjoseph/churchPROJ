from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Family
from django.utils import timezone
from .serializer import FamilySerializer


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
