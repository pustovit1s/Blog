from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    """ class for creating map of site"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        """transmits queryset posts into sitemap"""
        return Post.published.all()
    
    def lastmod(self, obj):
        """method which return time of last object change"""
        return obj.updated