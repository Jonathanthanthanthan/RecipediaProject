from django.urls import path
from . import views

app_name='RecipeSearcher'

urlpatterns = [
    path('',views.home ),

]