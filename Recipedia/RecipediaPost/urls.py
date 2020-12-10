#from django.urls import path
#from . import views
from django.contrib import admin
from django.urls import path
from app01 import views
from django.conf.urls import url
app_name = 'blog'
urlpatterns = [ # post views
               path('admin/', admin.site.urls),
               path('', views.post_list, name='post_list'), path('<int:year>/<int:month>/<int:day>/<slug:post>/',
                views.post_detail, name='post_detail'),
               url(r'^publish/', views.publish),#post a blog
               ]
