from django.urls import path, re_path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categories/<int:num>/',views.category,name ='category'),
    path('tags/<int:num>',views.tag,name='tag')
]
