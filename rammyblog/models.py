from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
import datetime, random
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from markdown import markdown
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField # <---
from markdownx.utils import markdownify # <---


class Blogpost(models.Model):
	author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
	title = models.CharField(max_length = 200)
	content = models.TextField(max_length=40000)
	tags = models.CharField(max_length = 50, default = 'uncategorized')
	created_date = models.DateTimeField(default = timezone.now)
	pub_date = models.DateTimeField(blank = True, null= True)
	updated = models.DateTimeField(auto_now = True)
	slug = models.SlugField(blank = True, null = True)


	def publish(self):
		self.pub_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

	@property
	def formatted_markdown(self):
		return markdownify(self.content)

	def get_message_as_markdown(self):
         return mark_safe(markdown(self.content, safe_mode='escape'))


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	about = models.TextField(max_length = 10000)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	website = models.URLField()
	phone = models.IntegerField(default = 0)
	city = models.CharField(max_length = 50, blank = True)



	def __str__(self):
		return self.user.username



class Comment(models.Model):
    comment = models.TextField(max_length=4000)
    topic = models.ForeignKey(Blogpost, related_name='comments', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete = models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete = models.CASCADE)
    active = models.BooleanField(default=True)
    photo = models.ForeignKey(UserProfile, on_delete =models.CASCADE)

    def __str__(self):
       return self.message

def blog_pre_save(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(blog_pre_save, sender=Blogpost)

def user_post_save(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(user_post_save, sender=User)