#Form: Allows you to build standard forms
from django import forms
from django.utils import timezone
from .models import Post, Comment
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
        widgets={
            'body':forms.Textarea(attrs={'class':'form-control', 'id':'exampleFormControlTextarea1'}),
            'title':forms.TextInput(attrs={'class':'form-control'}),
            }

class CommentForm(forms.ModelForm):
    class Meta:
            model = Comment
            fields = ('body',)

        
        

