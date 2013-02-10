from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Champion(models.Model):
	name = models.CharField(max_lenght=255)
	subscribers = models.ManyToManyField(User, through = 'Subscription')
