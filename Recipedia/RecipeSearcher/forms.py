from dal import autocomplete
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile

from django.urls import reverse
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth','bio', 'photo')

class SearchForm(forms.Form):
    Diet=[('balanced','Balanced'),('high-protein','High-Protein'),('low-fat','Low-Fat')]
    Health=[('alcohol-free','Alcohol-free'),('sugar-conscious','Sugar-conscious'),('peanut-free','Peanut-free'),('tree-nut-free','Tree Nuts'),('vegan','Vegan'),('vegetarian','Vegetarian')]
    keyword = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter list of ingredients seperated by commas'}))
    calories = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'step': '50', 'min': '0', 'max': '3000', 'class':'custom-range', 'id':'myRange', 'value':'1200'}), required=False, label='Max calories /Serving')
    maxNumberOfIngredients=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'id':'typeNumber','placeholder':'Number of ingredients'}),required=False)
    HealthLabels=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=Health, required=False,label='Health Labels')
    DietLabels=forms.MultipleChoiceField(choices=Diet,widget=forms.CheckboxSelectMultiple(), required=False,label='Diet Labels')
# Create your models here.

def labelParser(Label,LabelIdentifier):
    returnString=''
    for l in Label:
        returnString=returnString+'&'+LabelIdentifier+'='+l
    LabelString=str(Label)
    print(returnString)
    return returnString

def StringLabelParser(Label):
    returnString=''
    for l in Label:
        returnString=returnString+l+', '
    return returnString

class ProfileSearchForm(forms.ModelForm):
    user = forms.ModelChoiceField(
    queryset=get_user_model().objects.all(),
    widget=autocomplete.Select2(
        url='RecipeSearcher:user-autocomplete',
        attrs={'data-minimum-input-length': 1, 'class':'form-control', 'data-html':True})
)

    class Meta:
        model=User
        fields=('user',)
        
 


