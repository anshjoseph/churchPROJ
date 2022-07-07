from django.contrib import admin
from .models import (
    Session,
    LoginMaster
)
# Register your models here.


admin.site.register(Session)
admin.site.register(LoginMaster)