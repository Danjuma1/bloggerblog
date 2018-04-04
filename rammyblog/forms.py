from django import forms
from .models import Blogpost, Comment, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):
	class Meta:
		model = Blogpost
		fields = ['title','content','tags']

class CommentForm(forms.ModelForm):
	message = forms.CharField(max_length = 5000, widget = forms.Textarea(attrs = {'class':"form-control", 'rows':"3",}))
	class Meta:
		model = Comment
		fields = ['message']

	

class Register(UserCreationForm):
	first_name= forms.CharField(max_length = 50,)
	last_name= forms.CharField(max_length = 50,)
	email=forms.EmailField(max_length = 100, help_text = 'Enter a valid E-mail Address')
	class Meta:
		model = User
		fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = [ 'website', 'about', 'city', 'phone',]


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()