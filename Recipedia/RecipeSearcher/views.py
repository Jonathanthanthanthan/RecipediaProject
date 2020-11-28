from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm
from .models import Profile

def home(request):
    return render(request, 'index.html' )

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
            return render(request,'register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'register.html',{'user_form': user_form})

def profile(request, searchedUser):
    searchedUser = get_object_or_404(User,username=searchedUser)
    if searchedUser is not None:
        return render(request, 'profile.html', {'searchedUser':searchedUser})
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
    return render(request, 'edit.html', {'user_form':user_form, 'profile_form': profile_form})