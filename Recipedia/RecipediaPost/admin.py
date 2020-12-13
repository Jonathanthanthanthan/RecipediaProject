
from django.contrib import admin
from .models import Post
from .models import Post, Comment
#from django.conf import settings


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','publish','postdate','status','slug', 'photo')
    #ordering and searching function
    search_fields = ('title', 'body')
    ordering = ('status', 'publish')
    list_filter = ('status', 'created', 'publish', 'author')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish' 
    ordering = ('status', 'publish')

#manage comments through a simple interface.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'email', 'body')
