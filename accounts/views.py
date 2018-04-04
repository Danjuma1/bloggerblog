from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from accounts.forms import SignupForm
from django.urls import reverse_lazy
from  django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from rammyblog import views

def signup(request):
	if request.method =='POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect ('index')

	else:
		form = SignupForm()
	context  = {'form' :form}
	return render(request, 'boards/signup.html', context)

@method_decorator(login_required, name = 'dispatch' )
class AccountUpdate(UpdateView):
	model = User
	template_name = 'rammyblog/account_settings.html'
	fields = ['first_name' , 'last_name', 'email', ]
	success_url = reverse_lazy('accountupdate')

	def get_object(self):
		return self.request.user


