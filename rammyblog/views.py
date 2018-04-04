from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Blogpost, Comment, UserProfile
from django.utils import timezone
from .forms import PostForm, Register, CommentForm, UserProfileForm, ImageUploadForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from  django.utils.decorators import method_decorator

#from django.views.generic import ListView
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(ListView):
	model = Blogpost
	template_name = 'rammyblog/index.html'
	context_object_name = 'posts'
	paginate_by = 10

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pub_date__lte = timezone.now() ).order_by('-pub_date')

"""def index(request):
	post = Blogpost.objects.filter(pub_date__lte = timezone.now() ).order_by('-pub_date')
	context = {'post':post}
	return render(request, 'rammyblog/index.html', context)"""

def tags(request, post_tags):
	tags_posts = Blogpost.objects.filter(tags = post_tags)
	print (tags_posts)
	context = {'tags_posts': tags_posts}
	return render(request, 'rammyblog/tags.html', context)

def details(request, post_slug):
	post =  get_object_or_404(Blogpost, slug = post_slug)
	comments = post.comments.filter(active = True).order_by('-created_at')
	#pic = UserProfile.objects.get(user = )
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit = False)
			new_comment.post = post
			new_comment.created_by = request.user
			new_comment.topic_id = post.pk
			new_comment.photo_id = request.user.pk
			new_comment.save()
			return redirect('details', post_slug)
	else:
		form = CommentForm()
	#bio = UserProfile.objects.filter(user = )
	context = {'post': post, 'form':form, 'comments':comments,}
	return render(request, 'rammyblog/details.html', context)

@login_required
def comment_delete(request, comment_id, post_slug):
	comment = get_object_or_404(Comment, pk =comment_id)
	post = get_object_or_404(Blogpost, slug = post_slug)
	if request.method == 'POST':
		comment.delete()
		return redirect('details', post.slug )

	context = {'comment':comment}
	return render(request, 'rammyblog/comment_delete.html', context)
"""
def comment_pics(request, comment_id):
	comment = get_object_or_404(Comment, pk =comment_id)
	print(comment.created_by)
	picture = get_object_or_404(UserProfile, user = comment.created_by)
	print (picture.picture)
	context = {'picture':picture}
	return render(request, 'rammyblog/details.html', context)"""

@login_required
def comment_edit(request, comment_id, post_slug):
	comment = get_object_or_404(Comment, pk = comment_id)
	post = get_object_or_404(Blogpost, slug = post_slug)
	if request.method == 'POST':
		form = CommentForm(request.POST, instance = comment)
		if form.is_valid():
			new_comment = form.save(commit = False)
			new_comment.post = post
			new_comment.created_by = request.user
			new_comment.topic_id = post.pk
			new_comment.photo_id = request.user.pk
			new_comment.save()
			return redirect('details', post.slug)
	else:
		form = CommentForm(instance = comment)
	context = {'form':form, 'comment':comment}
	return render(request, 'rammyblog/comment_edit.html', context)


@login_required
def new_post(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('details', post.slug)
	else:
		form = PostForm()
	context = {'form': form}
	return render(request, 'rammyblog/new_post.html', context)

@login_required
def post_edit(request, post_slug):
	post_edit = get_object_or_404(Blogpost, slug = post_slug)
	if request.method == 'POST':
		form = PostForm(request.POST, instance = post_edit)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('details', post.slug)
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
def post_publish(request, post_slug):
	post = get_object_or_404(Blogpost, slug = post_slug)
	post.publish()
	return redirect('details', post.slug)

@login_required
def post_delete(request, post_slug):
	post = get_object_or_404(Blogpost, slug = post_slug)
	if request.method == 'POST':
		post.delete()
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


def search(request):
	try:
		if request.method == 'GET':
			new_search = Blogpost.objects.filter(Q(title__icontains = request.GET['q']) |
		 Q(content__icontains= request.GET['q']) | Q(tags__icontains = request.GET['q']) ).exclude(
		 pub_date__isnull = True
				)
		if new_search:
			context = {'new_search':new_search}
			return render(request, 'rammyblog/search.html', context)
		else:
			return render(request, 'rammyblog/404.html')

	except MultiValueDictKeyError as e:
		return render(request, 'rammyblog/404.html')

@login_required
def profile(request, username):
	author = get_object_or_404(User, username = username)
	bio = UserProfile.objects.filter(user = author)
	posts = Blogpost.objects.filter(author = author).exclude(pub_date__isnull = True)
	context = {'posts':posts, 'bio':bio, 'author':author}
	return render(request, 'rammyblog/profile_page2.html', context)

@login_required
def accountupdate(request):
	user = get_object_or_404(UserProfile, user = request.user)
	if request.method == 'POST':
		form = UserProfileForm(request.POST, instance = user)
		if form.is_valid():
			form.save(commit = False)
			website = form.cleaned_data['website']
			city = form.cleaned_data['city']
			about = form.cleaned_data['about']
			profile = UserProfile.objects.get(user = request.user)
			profile.website = website
			profile.city = city
			profile.about = about
			profile.save()
			form.save()
			return redirect('profile', request.user)

	else:
		form = UserProfileForm(instance =user)
	context = {'form':form}
	return render (request, 'rammyblog/profile_edit.html', context)

def upload_pics(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = get_object_or_404(UserProfile, user = request.user)
            m.picture = form.cleaned_data['image']
            m.save()
            return redirect('profile', request.user)
    return HttpResponseForbidden('allowed only via POST')
