#Form: Allows you to build standard forms
from django import forms
from django.utils import timezone
from .models import Post
from django.utils.text import slugify

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields= ('title','photo','body','status')

        
        

