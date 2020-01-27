from django.contrib import admin
from blog.models import Category,Tag,Post
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
class TagAdimin(admin.ModelAdmin):
    list_display = ['name']
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','body','excerpt','category','author','created_time','modified_time']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdimin)
admin.site.register(Post,PostAdmin)