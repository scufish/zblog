from django.urls import path, re_path
from resources import views

app_name = 'resources'

urlpatterns = [
    path('resource_signin/', views.resource_signin, name='resource_signin'),
    path('resource/',views.resource),
    path('quit/',views.quit),
    path('register/',views.register)
]
