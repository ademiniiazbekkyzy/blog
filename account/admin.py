from django.contrib import admin

# Register your models here.
from account.models import CustomUser

admin.site.register(CustomUser)