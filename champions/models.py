from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from datetime import date
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

from django.core import urlresolvers

class Product(models.Model):
	'''Generic representation of anything that can go on sale'''
	objects = InheritanceManager()
	subscribers = models.ManyToManyField(User, through='accounts.Subscription', related_name='products')
	name = models.CharField(max_length=255)
	slug = models.SlugField(blank=True, unique=True)

	def classname(self):
		'''Returns the name of this class for use in templates'''
		return self.__class__.__name__

	@property
	def active_sale_items(self):
		'''SaleItems that apply to this product and are active'''
		today = date.today()
		return self.sale_items.filter(sale__start__lte=today, sale__end__gte=today).order_by('-price').all()

	@property
	def active_sales(self):
		'''Sales that apply to this product and are active'''
		today = date.today()
		return self.sales.filter(start__lte=today, end__gte=today).all()

	@property
	def price(self):
		'''Returns the best price from active sales'''
		items = self.active_sale_items
		if len(items) > 0:
			return items[0].price
		return None

	@property
	def sale_start(self):
		'''Returns the start time of the best sale'''
		items = self.active_sale_items
		if len(items) > 0:
			return items[0].sale.start
		return None

	@property
	def sale_end(self):
		'''Returns the end time of the best sale'''
		items = self.active_sale_items
		if len(items) > 0:
			return items[0].sale.end
		return None

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return urlresolvers.reverse('champions_product',
			args=(self.slug,))

# Create your models here.
class Champion(Product):
	'''Represents a champion from the game'''
	product = models.OneToOneField(Product, parent_link=True)

	title = models.CharField(max_length=255)
	detail_url = models.URLField(max_length=1024)
	icon_url = models.URLField(max_length=1024)
	image_url = models.URLField(max_length=1024)
	short_description = models.TextField()
	description = models.TextField()

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return urlresolvers.reverse('champions_champion',
			args=(self.slug,))

class Skin(Product):
	'''Represents a particular skin for a champion'''
	product = models.OneToOneField(Product, parent_link=True, db_column='product_ptr_id')
	champion = models.ForeignKey(Champion, related_name='skins')

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return urlresolvers.reverse('champions_skin',
			args=(self.slug,))

class Sale(models.Model):
	'''A group of price changes with a name and start/end dates'''
	name = models.CharField(max_length=255)
	products = models.ManyToManyField(Product, related_name='sales', through='SaleItem')
	start = models.DateField()
	end = models.DateField()

	def __unicode__(self):
		return '{} ({}-{})'.format(self.name, self.start.strftime('%b. %d'),
									self.end.strftime('%b. %d'))


class SaleItem(models.Model):
	'''
	Model representing the ManyToMany relation between Sales and Products
	'''
	sale = models.ForeignKey(Sale, related_name='sale_items')
	product = models.ForeignKey(Product, related_name='sale_items')
	price = models.DecimalField(max_digits=12, decimal_places=2)

	def __unicode__(self):
		return '{} ({} RP)'.format(self.product.name, self.price)

def _slugify_name(sender, instance, raw, using, **kwargs):
	instance.slug = slugify(instance.name)

pre_save.connect(_slugify_name, Product)
pre_save.connect(_slugify_name, Skin)
pre_save.connect(_slugify_name, Champion)
