from django.db import models
from django.contrib.auth.models import User

from champions.models import Product


class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='subscriptions')
    product = models.ForeignKey(Product, related_name='subscriptions')
