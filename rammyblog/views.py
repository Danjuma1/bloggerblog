from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
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
from .utils import get_read_time, count_words
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
	comments = post.comments.filter(active = True).order_by('-created_at').filter(parent = None)
	comment_all = post.comments.filter(active = True).order_by('-created_at')
	session_key = 'viewed_topic_{}'.format(post.slug)
	if not request.session.get(session_key, False):
		post.views+=1
		post.save()
		request.session[session_key] = True 	
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit = False)
			new_comment.post = post
			new_comment.created_by = request.user
			new_comment.topic_id = post.pk
			new_comment.photo_id = request.user.pk
			parent_obj = None
			try:
				new_comment.parent_id = int(request.POST.get("parent_id"))
			except:
				new_comment.parent_id = None
			if new_comment.parent_id:
				parent_qs = Comment.objects.filter(id  = new_comment.parent_id)
				if parent_qs.exists() and parent_qs.count()== 1:
					parent_obj = parent_qs.first()		

			new_comment.save()
			return redirect('details', post_slug)
	else:
		form = CommentForm()
	bio = get_object_or_404(UserProfile, user = post.author)
	context = {'post': post, 'form':form, 'comments':comments, 'bio':bio, 'comment_all':comment_all}
	return render(request, 'rammyblog/details.html', context)

@login_required
def comment_delete(request, comment_id, post_slug):
	comment = get_object_or_404(Comment, id =comment_id)
	post = get_object_or_404(Blogpost, slug = post_slug)
	if request.method == 'POST':
		comment.delete()
		return redirect('details', post.slug )

	context = {'comment':comment}
	return render(request, 'rammyblog/comment_delete.html', context)

@login_required
def comment_delete(request, comment_id, post_slug):
	comment = get_object_or_404(Comment, id =comment_id)
	post = get_object_or_404(Blogpost, slug = post_slug)
	if request.method == 'POST':
		comment.delete()
		return redirect('details', post.slug )

	context = {'comment':comment}
	return render(request, 'rammyblog/comment_delete.html', context)

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
	comment = Comment.objects.filter(active = True).order_by('-created_at').filter(parent = None)
	comment_all = comment.filter(active = True).order_by('-created_at')
	print (posts)
	context = {'posts':posts, 'bio':bio, 'author':author, 'comment_all':comment_all}
	return render(request, 'rammyblog/profile_page_for_professionals.html', context)

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
			facebook_url = form.cleaned_data['facebook_url']
			twitter_url = form.cleaned_data['twitter_url']
			google = form.cleaned_data['google']
			profile = UserProfile.objects.get(user = request.user)
			profile.website = website
			profile.city = city
			profile.about = about
			profile.facebook_url = facebook_url
			profile.twitter_url = twitter_url
			profile.google = google
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

"""def comment_thread(request, pk):
	comment =get_object_or_404(Comment, pk = pk)
	#form = CommentForm(request.POST or None)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit = False)
			new_comment.post = post
			new_comment.created_by = request.user
			new_comment.topic_id = post.pk
			new_comment.photo_id = request.user.pk
			parent_obj = None
			try:
				new_comment.parent_id = int(request.POST.get("parent_id"))
			except:
				new_comment.parent_id = None
			if new_comment.parent_id:
				parent_qs = Comment.objects.filter(id  = new_comment.parent_id)
				if parent_qs.exists() and parent_qs.count()== 1:
					parent_obj = parent_qs.first()		

			new_comment.save()
			return redirect('details', post_slug)
	else:
		form = CommentForm()
	context = {'comment':comment, 'form':form}
	return render(request, 'rammyblog/comment_thread.html', context)"""