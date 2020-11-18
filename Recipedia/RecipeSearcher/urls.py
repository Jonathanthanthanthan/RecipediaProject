from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='RecipeSearcher'

urlpatterns = [
    path('',views.home ),
    path('login', views.userlogin),
    path('results', views.results),
    path('base', views.base),
    path('register', views.register)
]