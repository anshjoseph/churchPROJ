from django.contrib import admin

# importing model form ./models.py
from .models import Ward,Family,People

# Register models
admin.site.register(Ward)    # WARD model
admin.site.register(Family)  # FAMILY model
admin.site.register(People)  # PEOPLE model