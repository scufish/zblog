from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from django.views.decorators.http import require_POST
from .form import CommentForm
from django.contrib import messages

# Create your views here.

@require_POST
def comment(req,num):
    post =get_object_or_404(Post,pk =num)
    form = CommentForm(req.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post=post
        comment.save()
        messages.add_message(req,messages.SUCCESS,'评论发表成功',extra_tags='success')
        return redirect(post)
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(req, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
    return render(req, 'comments/preview.html', context=context)
