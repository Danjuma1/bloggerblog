from django.db import models
from django.utils import timezone

class Blogpost(models.Model):
	author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
	title = models.CharField(max_length = 200)
	content = models.TextField()
	tags = models.TextField(default = 'Test')
	created_date = models.DateTimeField(default = timezone.now)
	pub_date = models.DateTimeField(blank = True, null= True)
	def publish(self):
		self.pub_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title


# Create your models here.
