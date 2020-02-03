from django.db import models


# Create your models here.

class PrivateUser(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=30)
    email =  models.EmailField()
    object = models.Manager()
    class Meta:
        verbose_name = '资源分享权限用户'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username


class Resource(models.Model):
    subject = models.CharField(max_length=100)
    href = models.URLField()
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(PrivateUser,on_delete=models.CASCADE,verbose_name='提供者',default='')
    object = models.Manager()

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


