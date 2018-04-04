from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
	email = forms.CharField(max_length = 250, required = True, widget=forms.EmailInput())
	first_name = forms.CharField(max_length = 250, required = True, widget=forms.TextInput())
	last_name = forms.CharField(max_length = 250, required = True, widget=forms.TextInput())

	class Meta:
		model = User
		fields = ['username', 'first_name' , 'last_name', 'email', 'password1', 'password2']
