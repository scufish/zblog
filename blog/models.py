from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
import markdown
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False, null=False,verbose_name='分类')
    object = models.Manager()
    class Meta:
        verbose_name='分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False, null=False,verbose_name='标签')
    object = models.Manager()
    class Meta:
        verbose_name='标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Post(models.Model):
    #文章标题
    title = models.CharField(max_length=70,unique=True,blank=False,null=False,verbose_name='标题')
    #文本
    body=models.TextField(verbose_name='内容')
    #创造时间
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    #修改时间
    modified_time=models.DateTimeField(auto_now=True,verbose_name='修改时间')
    #摘要，允许为空
    excerpt=models.CharField(max_length=200,blank=True,verbose_name='摘要')
    #分类外键：级联删除
    category=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='分类')
    #多对多标签关系
    tags=models.ManyToManyField(Tag,blank=True,verbose_name='标签')
    #文章作者，这里 User 是从 django.contrib.auth.models 导入的。django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程。其中 User 是 django 为我们已经写好的用户模型，和我们自己编写的 Category 等类是一样的。这里我们通过 ForeignKey 把文章和 User关联了起来，因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author =models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')
    view =models.PositiveIntegerField(default=0,editable=False)
    object =models.Manager()
    class Meta:
        verbose_name='文章'
        #复数
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
    def add_view(self):
        self.view =self.view+1
        self.save(update_fields=['view'])
    #覆写save方法，自动填充摘要
    def save(self,*args,**kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite'
        ])
        if self.excerpt == '':
            #去掉html标签
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args,**kwargs)

class Message(models.Model):
    name = models.CharField(max_length=10)
    email =models.EmailField()
    subject =models.CharField(max_length=30)
    message =models.TextField()
    class Meta:
        verbose_name = '消息'
        # 复数
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.subject
