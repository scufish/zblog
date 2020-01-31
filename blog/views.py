from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from blog.models import Post,Category,Tag,Message
import markdown, re
from  django.contrib import messages

# Create your views here.

# 首页视图函数
def index(req):
    post_list = Post.object.all().order_by('-created_time')
    return render(req, 'blog/index.html', context={
        'post_list': post_list
    })


# 文章阅读页面视图函数
def detail(req, pk):
    # 获取失败则返回404.html
    post = get_object_or_404(Post, pk=pk)
    post.add_view()
    # 使用markdown解析body内容，这里使用了三个拓展，分别是 extra、codehilite、toc。extra 本身包含很多基础拓展，而 codehilite 是语法高亮拓展，这为后面的实现代码高亮功能提供基础，而
    # toc 则允许自动生成目录。
    # 注意markdown code代码块一定要缩进（四个空格）
    # 注意django 的模块变量默认转义，使用safe标签

    # markdown解析的第一个版本，直接使用markdown函数解析，返回html文本。
    # post.body=markdown.markdown(post.body,extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',
    #     'markdown.extensions.toc',
    # ])

    # 第二个版本：先创建Markdown类的对象并传入相关参数，接着使用对象的convert方法返回html文件。
    # 该对象还保存了toc属性，便于生成目录
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc', ])
    post.body = md.convert(post.body)
    # 注意这个 post 实例本身是没有 toc 属性的，我们给它动态添加了 toc 属性，这就是 Python 动态语言的好处
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(req, 'blog/detail.html', context={
        'post': post
    })


def archive(req, year, month):
    post_list = Post.object.filter(created_time__year=year,created_time__month =month).order_by('-created_time')
    return render(req, 'blog/index.html', {
        'post_list': post_list
    })


def category(req,num):
    cate = Category.object.get(pk=num)
    post_list = Post.object.filter(category=cate).order_by('-created_time')
    return render(req,'blog/index.html',{
        'post_list': post_list
    })

def tag(req,num):
    t =Tag.object.get(pk=num)
    post_list = Post.object.filter(tags=t).order_by('-created_time')
    return render(req,'blog/index.html',{
        'post_list': post_list
    })


def about(req):
    return render(req,'blog/about.html',{})


def contact(req):
    return render(req,'blog/contact.html',{})

def resource(req):
    return render(req,'blog/resource.html',{})

def send_message(req):
    q =req.POST
    m =Message()
    m.name = q['name']
    m.email =q['email']
    m.subject = q['subject']
    m.message =q['message']
    m.save()
    messages.add_message(req, messages.SUCCESS, '消息发送成功', extra_tags='success')
    return redirect('/')