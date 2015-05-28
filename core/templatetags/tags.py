from django import template
import datetime
import memcache
from django.core.cache import cache

register = template.Library()

def show_tags():
    tags = cache.get('tags')

    return {'tags': tags}

def show_users():
    users = cache.get('users')
    
    return {'users': users}


register.inclusion_tag('users_template.html')(show_users)
register.inclusion_tag('tags_template.html')(show_tags)


