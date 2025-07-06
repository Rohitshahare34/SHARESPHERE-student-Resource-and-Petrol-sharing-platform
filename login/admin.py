
from django.contrib import admin
from BuySell.models import Items
from login.models import Users

admin.site.register(Items)
admin.site.register(Users)