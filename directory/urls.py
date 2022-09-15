from .views import (
    ChurchDirectoryEndpoint,
    FamilyMembersEndpoint,
    FamilySigninEndpoint,
    FamilySignupEndpoint,
    WardListEndpoint,
    FamilyUpdateEndpoint,
    FamilyDescriptionEndpoint,
)
from django.urls import path


urlpatterns = [
    path(
        "sign-in/",
        FamilySigninEndpoint.as_view(),
    ),
    path(
        "sign-up/",
        FamilySignupEndpoint.as_view(),
    ),
    path(
        "wards/",
        WardListEndpoint.as_view(),
    ),
    path(
        "families/",
        ChurchDirectoryEndpoint.as_view(),
    ),
    path(
        "family/<int:pk>/",
        FamilyDescriptionEndpoint.as_view(),
    ),
    path(
        "family/update/",
        FamilyUpdateEndpoint.as_view(),
    ),
    path(
        "family/members/",
        FamilyMembersEndpoint.as_view(),
    ),
    path(
        "family/members/<int:pk>/",
        FamilyMembersEndpoint.as_view(),
    ),
]
