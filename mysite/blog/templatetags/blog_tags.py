import markdown
from django.utils.safestring import mark_safe
from django import template
from django.db.models import Count

from blog.models import PublishedManager
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    """ tag which count number of posts"""
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """ tag for showing latest posts"""
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5) -> PublishedManager:
    """tag for showing most commented posts"""
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    """tsg filter for markdown format"""
    return mark_safe(markdown.markdown(text))
