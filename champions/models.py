from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
	subscribers = models.ManyToManyField(User, through='accounts.Subscription', related_name='products')
	determiner = models.IntegerField(default=0)

	@property
	def child(self):
		if self.determiner == 1:
			return self.champion
		else:
			return self._set_determiner()

	def _set_determiner(self):
		try:
			child = self.champion
			self.determiner = 1
			return child
		except Champion.DoesNotExist:
			pass

		try:
			child = self.skin
			self.determiner = 2
			return child
		except Skin.DoesNotExist:
			pass

		return None # No product attached? Probably an error...

	def save(self, *args, **kwargs):
		self._set_determiner()
		return super(Product, self).save(*args, **kwargs)

# Create your models here.
class Champion(Product):
	product = models.OneToOneField(Product, parent_link=True)

	name = models.CharField(max_length=255, unique=True)
	title = models.CharField(max_length=255)
	detail_url = models.URLField(max_length=1024)
	icon_url = models.URLField(max_length=1024)
	image_url = models.URLField(max_length=1024)
	short_description = models.TextField()
	description = models.TextField()

class Skin(Product):
	name = models.CharField(max_length=255)
	champion = models.ForeignKey(Champion)
