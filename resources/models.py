from django.db import models

# Create your models here.


class Resource(models.Model):
    subject = models.CharField(max_length=100)
    href =models.URLField()
    created_time =models.DateTimeField(auto_now_add=True)
    object = models.Manager()
    class Meta:
        verbose_name = '资源'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.subject