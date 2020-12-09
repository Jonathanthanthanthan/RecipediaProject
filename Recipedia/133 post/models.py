from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#the following lines to be added to the models.py file of the blog application
class Post(models.Model):
    STATUS_CHOICES = (
                      ('draft', 'Draft'),
                      ('published', 'Published'),
    )
    #This is the field for the post title
    title = models.CharField(max_length = 250)
    postdate = models.DateField(blank = True, null = True)
    #This field defines a many-to-one relationship, meaning that each post is written by a user,
    #and a user can write any number of posts.
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    #This is the body of the post.
    body = models.TextField()
    status = models.CharField(max_length = 128,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta
        ordering = ('-publish')
    
    def __str__(self):
        return self.title

