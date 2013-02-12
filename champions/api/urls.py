from django.conf.urls.defaults import url, patterns, include
from .resources import ProductResource, SkinResource, ChampionResource, SaleResource, SaleItemResource

product_resource = ProductResource()
sale_resource = SaleResource()
sale_item_resource = SaleItemResource()
skin_resource = SkinResource()
champion_resource = ChampionResource()

urlpatterns = patterns('',
    url(r'^', include(product_resource.urls)),
    url(r'^', include(skin_resource.urls)),
    url(r'^', include(champion_resource.urls)),
    url(r'^', include(sale_resource.urls)),
    url(r'^', include(sale_item_resource.urls)),
)
