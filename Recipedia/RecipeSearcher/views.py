from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.html import format_html
from .forms import *
from .models import Profile, Contact
from datetime import date
from RecipediaPost.models import Post
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
import http.client
import json
from dal import autocomplete
import unicodedata

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def results(request):
    if request.method == "POST":
        search_form=SearchForm(data=request.POST)
        if search_form.is_valid():
            cd=search_form.cleaned_data
            request.session['DietLabel']=cd['DietLabels']
            request.session['HealthLabel']=cd['HealthLabels']
            request.session['keyword']=cd['keyword']
            request.session['cals']=cd['calories']
            request.session['maxIngredients']=cd['maxNumberOfIngredients']
            response=redirect('RecipeSearcher:results')
            return response
    else:
        search_form=SearchForm()
        conn = http.client.HTTPSConnection("rapidapi.p.rapidapi.com")
        searchString='/search?q='
        headers = {
            'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com",
            'x-rapidapi-key': "03e7e0d99cmshf91be55a6500328p140583jsn8da2cf74d30b"
            }
        keyword=request.session.get('keyword')
        keyword=keyword.replace(" ","")
        keyword=keyword.strip()
        keyword=remove_control_characters(keyword)
        print(keyword)
        searchString=searchString+keyword+'&from=0&to=100'
        if request.session.get('cals') is not None:
            cals=request.session.get('cals')
            searchString=searchString+'&calories=0-'+str(cals)
        if request.session.get('maxIngredients') is not None or 0:
            maxIngredients=request.session['maxIngredients']
            searchString=searchString+'&ingr='+str(maxIngredients)
        if request.session.get('DietLabel') is not None:
            DietLabel=request.session['DietLabel']
            LabelIdentifier='diet'
            searchString=searchString+labelParser(DietLabel,LabelIdentifier)
        if request.session.get('HealthLabel') is not None:
            HealthLabel=request.session['HealthLabel']
            LabelIdentifier='health'
            searchString=searchString+labelParser(HealthLabel,LabelIdentifier)
        conn.request("GET", searchString, headers=headers)
        print(searchString)
        res = conn.getresponse()
        raw_data = res.read()
        json_data=json.loads(raw_data)
        hits = json_data['hits']
        hitCount=len(hits)
        listOfRecipes=[]
        for recipes in hits:
            listOfRecipes.append(recipes['recipe'])
            
        paginator=Paginator(listOfRecipes, 30)
        page = request.GET.get('page')
        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            recipes =paginator.page(1)
        except EmptyPage:
            recipes =paginator.page(paginator.num_pages)
        return render(request,'results.html', {'page':page, 'recipes':recipes, 'search_form':search_form, 'hitCount':hitCount, 'dietLabelData':StringLabelParser(request.session.get('DietLabel')),'healthLabelData':StringLabelParser(request.session.get('HealthLabel'))})

def home(request):
    if request.method == "POST":
        search_form=SearchForm(data=request.POST)
        if search_form.is_valid():
            cd=search_form.cleaned_data
            request.session['DietLabel']=cd['DietLabels']
            request.session['HealthLabel']=cd['HealthLabels']
            request.session['keyword']=cd['keyword']
            request.session['cals']=cd['calories']
            request.session['maxIngredients']=cd['maxNumberOfIngredients']
            response=redirect('RecipeSearcher:results')
            return response
    else:
        search_form=SearchForm()
    return render(request,'index.html',{'search_form':search_form})

def userlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('RecipeSearcher:home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'userlogin.html', {'form': form})


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

def following_list (request, searchedUser):
    user = get_object_or_404(User,username=searchedUser)
    return render(request, 'profile/following_list.html', {'user':user})

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

class UserAutocomplete(autocomplete.Select2QuerySetView):
    choice_template = 'userchoice.html'

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        return qs
    def get_result_label(self, item):
        return '@'+item.username

@login_required
def userSearch(request):
    if request.method == 'GET':
        profileSearchForm=ProfileSearchForm(data=request.GET)
        if profileSearchForm.is_valid():
            selectedUser=profileSearchForm.cleaned_data['user']
            return redirect('RecipeSearcher:profile_page',searchedUser= selectedUser)
        else:
            print(profileSearchForm.errors)
    else:
        profileSearchForm=ProfileSearchForm()
    return render(request,'usersearch.html', {'profileSearchForm':profileSearchForm})