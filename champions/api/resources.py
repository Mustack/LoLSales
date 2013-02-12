from django.contrib.auth.models import User
from tastypie.authentication import SessionAuthentication,  \
                                    BasicAuthentication,    \
                                    MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.resources import ModelResource

from champions.models import Product, Skin, Champion, Sale, SaleItem

def resource_meta(model, name=None, queryset=None,
                    authentication=None, authorization=None):
    '''Shortcut for building Meta classes for ModelResources'''
    if not name:
        name = model.__name__.lower()

    if not queryset:
        queryset = model.objects.all()

    if not authentication:
        authentication = MultiAuthentication(SessionAuthentication(),
                                                BasicAuthentication())

    if not authorization:
        authorization = DjangoAuthorization()

    obj = {
        'queryset': queryset,
        'resource_name': name,
        'authentication': authentication,
        'authorization': authorization
    }
    return type('Meta', tuple(), obj)

class ProductResource(ModelResource):
    Meta = resource_meta(Product)
    champion = fields.ForeignKey('champions.api.resources.ChampionResource',
                                    'champion', null=True)
    skin = fields.ForeignKey('champions.api.resources.SkinResource',
                                'skin', null=True)

class ChampionResource(ModelResource):
    Meta = resource_meta(Champion)
    skins = fields.ToManyField('champions.api.resources.SkinResource',
                                'skins')

class SkinResource(ModelResource):
    Meta = resource_meta(Skin)
    champion = fields.ForeignKey(ChampionResource, 'champion')

class SaleResource(ModelResource):
    Meta = resource_meta(Sale)
    sale_items = fields.ToManyField('champions.api.resources.SaleItemResource',
                                'sale_items')

class SaleItemResource(ModelResource):
    Meta = resource_meta(SaleItem)
    sale = fields.ForeignKey(SaleResource, 'sale')
    product = fields.ForeignKey(ProductResource, 'product')
