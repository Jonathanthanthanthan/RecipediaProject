from django.urls import path
from . import views

app_name='RecipeSearcher'

urlpatterns = [
    path('',views.home ),
    path('login', views.login),
    path('results', views.results),
    path('base', views.base)

]