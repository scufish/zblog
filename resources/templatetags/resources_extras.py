from resources.models import Resource
from django import template

register  = template.Library()

@register.inclusion_tag('resources/inclusions/_resource_recent.html', takes_context=True)
def show_recent_resources(context, num=3):
    return {
        'resources_list': Resource.object.all().order_by('-created_time')[:num]
    }

@register.inclusion_tag('resources/inclusions/_resource.html', takes_context=True)
def show_resources(context):
    return {
        'resources_list': Resource.object.all().order_by('tag')
    }
@register.inclusion_tag('resources/inclusions/_submit.html',takes_context=True)
def show_submit(context):
    return {}