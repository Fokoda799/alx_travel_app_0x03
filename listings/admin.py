from django.contrib import admin
from .models import CustomUser, Listing, Payment

# Register your models here.
# Mange users models
admin.site.register(CustomUser)
admin.site.register(Listing)
admin.site.register(Payment)