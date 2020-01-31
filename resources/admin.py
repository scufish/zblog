from django.contrib import admin
from .models import Resource

# Register your models here.
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ['subject','href']

admin.site.register(Resource,ResourcesAdmin)