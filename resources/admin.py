from django.contrib import admin
from .models import Resource,PrivateUser

# Register your models here.
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ['subject','href']

class PrivateUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password']

admin.site.register(Resource,ResourcesAdmin)
admin.site.register(PrivateUser,PrivateUserAdmin)