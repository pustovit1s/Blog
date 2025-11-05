"""models for blog aplication"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """class for publishing posts"""
    def get_queryset(self):
        """function return queryset"""
        return super().get_queryset()\
                        .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """class of posts model"""

    class Status(models.TextChoices):
        """class for status of post"""
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                                            unique_for_date='publish')
    author = models.ForeignKey(User,
                                            on_delete=models.CASCADE,
                                            related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                                                choices=Status.choices,
                                                default=Status.DRAFT)
    tags = TaggableManager()


    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        """ meta class for ordering posts"""
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        """function return title"""
        return self.title

    def get_absolute_url(self):
        """revers url function"""
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])



class Comment(models.Model):
    """class for comments model"""
    post = models.ForeignKey(Post,
                                         on_delete=models.CASCADE,
                                         related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        """meta class for comments ordering"""
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
