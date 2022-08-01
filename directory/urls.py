from .views import FamilySigninEndpoint, FamilySignupEndpoint
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
]
