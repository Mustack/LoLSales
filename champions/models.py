from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Champion(models.Model):
	subscribers = models.ManyToManyField(User, through = 'accounts.Subscription')

	name = models.CharField(max_length=255, unique=True)
	title = models.CharField(max_length=255)
<<<<<<< HEAD

	subscribers = models.ManyToManyField(User, through='accounts.Subscription', related_name='champions')
=======
	detail_url = models.URLField(max_length=1024)
	icon_url = models.URLField(max_length=1024)
	image_url = models.URLField(max_length=1024)
	short_description = models.TextField()
	description = models.TextField()
>>>>>>> 0e384265b88364d1aa403110e5ca34c800bebf8c
