from django.conf.urls import patterns, url
from .views import SearchView, ChampionView, ProductView

urlpatterns = patterns('',
	url(r'^search/', SearchView.as_view(), name='champions_search'),
	url(r'^product/(?P<slug>[-_\w]+)/$', ProductView.as_view(), name='champions_product'),
	url(r'^champion/(?P<slug>[-_\w]+)/$', ChampionView.as_view(), name='champions_champion'),
	url(r'^skin/(?P<slug>[-_\w]+)/$', ChampionView.as_view(), name='champions_skin'),
)
