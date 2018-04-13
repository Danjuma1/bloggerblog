from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
import datetime, random
from django.db.models.signals import pre_save, post_save, post_delete
from .utils import unique_slug_generator
from markdown import markdown
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField # <---
from markdownx.utils import markdownify # <---
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager
from .utils import get_read_time

class Blogpost(models.Model):
	author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
	title = models.CharField(max_length = 200)
	content = models.TextField(max_length=40000)
	tags = models.CharField(max_length=200, blank=True, default = "uncategorized")
	created_date = models.DateTimeField(default = timezone.now)
	pub_date = models.DateTimeField(blank = True, null= True)
	read_time = models.IntegerField(default = 0)
	updated = models.DateTimeField(auto_now = True)
	slug = models.SlugField(blank = True, null = True)
	views = models.IntegerField(default = 0)
	#topic = models.ForeignKey(Comment, related_name='comments', on_delete = models.CASCADE)

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
	picture = models.ImageField(upload_to='profile_images')
	website = models.URLField()
	facebook_url = models.URLField(default ='http://www.facebook.com')
	twitter_url = models.URLField(default ='http://www.twitter.com')
	google = models.URLField(default ='http://www.googleplus.com')
	phone = models.IntegerField(default = 0)
	city = models.CharField(max_length = 50, blank = True)

	def picture_or_default(self, default_path="media\profile_images\profile.jpg"):
		if self.picture:
			return self.picture
		return default_path



	def __str__(self):
		return self.user.username

	def file_size(value):
		limit = 2 * 1024 * 1024
		if value.size > limit:
			raise ValidationError('File too large. Size should not exceed 2 MiB.')

"""class CommentManager(models.Manager):
	def all(self):
		qs = super(CommentManager, self).filter(parent = None)
		return qs
	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		obj_id = instance.id
		qs =super(CommentManager, self).filter(content_type =content_type, object_id = obj_id).filter(parent = None)
		return qs"""

class Comment(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Blogpost, related_name='comments', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete = models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete = models.CASCADE)
    active = models.BooleanField(default=True)
    photo = models.ForeignKey(UserProfile, on_delete =models.CASCADE)
    parent = models.ForeignKey("self", null = True, blank = True, on_delete = models.SET_NULL)
    
    #objects = CommentManager()

    def __str__(self):
       return self.message
    class Meta:
    	ordering = ['-created_at']


    def children(self):
    	return Comment.objects.filter(parent = self)

    @property
    def is_parent(self):
    	if self.parent is not None:
    		return False
    	return True

def blog_pre_save(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
	if instance.content:
		html_string = instance.get_message_as_markdown()
		read_time = get_read_time(html_string)
		instance.read_time = read_time

pre_save.connect(blog_pre_save, sender=Blogpost)

def user_post_save(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(user_post_save, sender=User)
