from django import template
from ..form import CommentForm
from ..models import Comment
register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post
    }
@register.inclusion_tag('comments/inclusions/_list.html',takes_context=True)
def show_comments(context,post):
    comment_list = Comment.object.filter(post=post)
    comment_count=comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }