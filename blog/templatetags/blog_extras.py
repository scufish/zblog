from blog.models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count


register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_posts_list': Post.object.all().order_by('-created_time')[:num]
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.object.dates('created_time', 'month', order='DESC')
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.object.annotate(post_num=Count('post')).filter(post_num__gt=0)
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.object.annotate(post_num=Count('post'))
    }


