from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='RecipeSearcher'

urlpatterns = [
    path('',views.home ),
    path('login/', views.userlogin, name='login'),
    path('results/', views.results),
    path('base/', views.base),
    path('register/', views.register),
    path('edit/', views.edit),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<searchedUser>/', views.profile, name='profile_page'),
    path('<searchedUser>/followers/', views.followers_list, name='followers_list'),
    path('<searchedUser>/following/', views.following_list, name='following_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
]
