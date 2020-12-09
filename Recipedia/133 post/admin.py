
from django.contrib import admin
from .models import Post
#from django.conf import settings

@admin.register(Post)
class PostAdmin(models.Post):
    list_display = ('title','publisher','postdate','status')
    #ordering and searching function
    search_fields = ('title', 'body')
    ordering = ('status', 'publish')
