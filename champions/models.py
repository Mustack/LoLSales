from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
	subscribers = models.ManyToManyField(User, through='accounts.Subscription', related_name='products')

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

	def __unicode__(self):
		return self.name

class Skin(Product):
	product = models.OneToOneField(Product, parent_link=True, db_column='product_ptr_id')
	name = models.CharField(max_length=255)
	champion = models.ForeignKey(Champion)

	def __unicode__(self):
		return self.name

class Sale(models.Model):
	name = models.CharField(max_length=255)
	products = models.ManyToManyField(Product, related_name='sales', through='SaleItem')
	start = models.DateField()
	end = models.DateField()

class SaleItem(models.Model):
	sale = models.ForeignKey(Sale, related_name='sale_items')
	product = models.ForeignKey(Product, related_name='sale_items')
	price = models.DecimalField(max_digits=12, decimal_places=2)
