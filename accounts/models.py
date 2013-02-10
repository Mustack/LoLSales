from django.db import models
from django.contrib.auth.models import User

from .. import Champion
# Create your models here.

class Subscription(models.Model):
	user = models.ForeignKey(User)
	group = models.ForeignKey(Champion)
