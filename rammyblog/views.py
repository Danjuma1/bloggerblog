from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Blogpost
from django.utils import timezone
from .forms import PostForm, Register
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def index(request):
	post = Blogpost.objects.filter(pub_date__lte = timezone.now() ).order_by('-pub_date')
	context = {'post':post}
	return render(request, 'rammyblog/index.html', context)

def details(request, post_id):
	post = get_object_or_404(Blogpost, pk = post_id)
	context = {'post': post}
	return render(request, 'rammyblog/details.html', context)

@login_required
def new_post(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('details', post.pk)
	else:
		form = PostForm()
	context = {'form': form}
	return render(request, 'rammyblog/new_post.html', context)

@login_required
def post_edit(request, post_id):
	post_edit = get_object_or_404(Blogpost, pk = post_id)
	if request.method == 'POST':
		form = PostForm(request.POST, instance = post_edit)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('details', post.pk)
	else:
		form = PostForm(instance = post_edit)
	context = {'form': form}
	return render(request, 'rammyblog/new_post.html', context)

@login_required
def post_draft(request):
	draft = Blogpost.objects.filter(pub_date__isnull = True).filter(author = request.user).order_by('created_date')
	context = {'draft':draft}
	return render(request, 'rammyblog/post_draft.html', context)

@login_required
def post_publish(request, post_id):
	post = get_object_or_404(Blogpost, pk = post_id)
	post.publish()
	return redirect('details', post.pk)

@login_required
def post_delete(request, post_id):
	post = Blogpost.objects.get(pk= post_id)
	if request.method == 'POST':
		post.delete()
		messages.success(request, 'Profile details updated.')
		return redirect('index')
	context = {'post' :post}
	return render(request, 'rammyblog/confirm.html', context)

def register(request):
	if request.method == 'POST':
		form = Register(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate (username = username, password = password)
			login(request, user)
			return redirect('index')

	else:
		form = Register()
	context = {'form':form}
	return render(request, 'registration/register.html', context)

@login_required	
def admin_draft(request):
	draft = Blogpost.objects.filter(pub_date__isnull = True).order_by('-created_date')
	context = {'draft' : draft}
	return render(request, 'rammyblog/post_draft.html', context)



