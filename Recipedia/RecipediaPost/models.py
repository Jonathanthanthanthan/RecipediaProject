from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
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
    slug = models.SlugField(max_length=250,
                                unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #This is the body of the post.
    body = models.TextField()
    status = models.CharField(max_length = 128,
                              choices=STATUS_CHOICES,
                              default='draft')

    def get_absolute_url(self):
        return reverse('blog:post_detail',
               args=[self.publish.year,
                     self.publish.month,
                     self.publish.day, self.slug])

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    
    class Meta
        ordering = ('-publish')

#add the custom manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
                            .filter(status='published')

#build a model to store comments.
class Comment(models.Model):
    post = models.ForeignKey(Post,
                         on_delete=models.CASCADE,
                         related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


    
    def __str__(self):
        return self.title

