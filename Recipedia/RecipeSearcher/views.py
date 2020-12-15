from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from .forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm, SearchForm
from .models import Profile
from datetime import date
from RecipediaPost.models import Post

def home(request):

    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
    form = SearchForm(request.GET)
    if form.is_valid():
    query = form.cleaned_data['query']
    results = Post.published.annotate(
    search=SearchVector('title', 'body'),
    ).filter(search=query)
    return render(request,
    'index.html',
    {'form': form,
    'query': query,
    'results': results})

def userlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)

                    return render (request,'index.html')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'userlogin.html', {'form': form})

def results(request):
    return render(request,'results.html')

def base(request):
    return render(request,'base.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            subject='Recipedia account creation'
            message='Thank you, '+ new_user.first_name+' for creating an account at Recipedia. Your account was created on ' + date.today().strftime("%m/%d/%y") + ". Now that you're registered you can start searching for recipes or upload your own!"
            email=new_user.email
            send_mail(subject,message,email,[email])
            return render(request,'register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'register.html',{'user_form': user_form})

def profile(request, searchedUser):
    searchedUser = get_object_or_404(User,username=searchedUser)

    posts = Post.published.get_queryset(searchedUser)

    if searchedUser is not None:
        return render(request, 'profile/profile.html', {'searchedUser':searchedUser, 'posts':posts})
    else:
        response=redirect('register')
        return response

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)
    return render(request, 'profile/edit.html', {'user_form':user_form, 'profile_form': profile_form})
