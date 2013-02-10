from django.db import models
from django.contrib.auth.models import User

from champions.models import Champion


class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='subcriptions')
    champions = models.ForeignKey(Champion)
