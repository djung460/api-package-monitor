from django.contrib import admin
from api.models import User,Device,RequestLog


# Register your models here.
admin.site.register(User)
admin.site.register(Device)
admin.site.register(RequestLog)
