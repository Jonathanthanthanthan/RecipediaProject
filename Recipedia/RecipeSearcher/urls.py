from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from.views import UserAutocomplete

app_name='RecipeSearcher'

urlpatterns = [
    path('',views.home, name='home'),
    path('login/', views.userlogin, name='login'),
    path('results/', views.results, name='results'),
    path('base/', views.base),
    path('register/', views.register),
    path('edit/', views.edit),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('userSearch/', views.userSearch, name='userSearch'),
    path('user-autocomplete/',UserAutocomplete.as_view(),name='user-autocomplete'),
    path('<searchedUser>/', views.profile, name='profile_page'),
    path('<searchedUser>/followers/', views.followers_list, name='followers_list'),
    path('<searchedUser>/following/', views.following_list, name='following_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
   
]
