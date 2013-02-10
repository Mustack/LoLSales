from django.conf.urls import patterns, include, url

from django.contrib import admin
from djrill import DjrillAdminSite

from champions.views import ChampionView

admin.site = DjrillAdminSite()

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LoLSales.views.home', name='home'),
    # url(r'^LoLSales/', include('LoLSales.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^champion/', ChampionView.as_view()),
    url(r'^home/', 'pages.views.home'),
    url(r'^accounts/', include('accounts.urls')),
)
