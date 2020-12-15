from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from .forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm, SearchForm
from .models import Profile
from datetime import date
from RecipediaPost.models import Post
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
import http.client
import json

def home(request):
    text = ""
    # form = SearchForm()
    # keyword = ""
    # results = [] #work with project.py
    # if 'keyword' in request.GET:
    #     form = SearchForm(request.GET)
    #     print("got here")
    #     if form.is_valid():
    #         keyword = form.cleaned_data['query']
    #         print("keyword: ", keyword)

    if request.method == "POST":
        keyword = request.POST.get('keyword')
        print(keyword)
        conn = http.client.HTTPSConnection("rapidapi.p.rapidapi.com")
        headers = {
            'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com",
            'x-rapidapi-key': "03e7e0d99cmshf91be55a6500328p140583jsn8da2cf74d30b"
            }
        conn.request("GET", "/search?q="+keyword, headers=headers)
        res = conn.getresponse()
        raw_data = res.read()
        encoding = res.info().get_content_charset('utf8')  # JSON default
        data = json.loads(raw_data.decode(encoding))
        # create a formatted string of the Python JSON object
        text = json.dumps(data, sort_keys=True, indent=4)
        print(text)
    return render(request,'index.html')

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
    user = get_object_or_404(User,username=searchedUser)
    posts = Post.published.get_queryset(user)

    if searchedUser is not None:
        return render(request, 'profile/profile.html', {'user':user, 'posts':posts})
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


def followers_list (request, searchedUser):
    user = get_object_or_404(User,username=searchedUser)
    return render(request, 'profile/followers_list.html', {'user':user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})
