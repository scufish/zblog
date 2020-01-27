from django.urls import path, re_path
from . import views

app_name = 'comments'

urlpatterns = [
    path('comments/<int:num>/',views.comment,name='comment')
]
