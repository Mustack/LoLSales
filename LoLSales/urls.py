from django.conf.urls import patterns, include, url

import autocomplete_light
from django.contrib import admin
from djrill import DjrillAdminSite

admin.site = DjrillAdminSite()


autocomplete_light.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LoLSales.views.home', name='home'),
    # url(r'^LoLSales/', include('LoLSales.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^$', 'pages.views.home'),

    url(r'autocomplete/', include('autocomplete_light.urls')),

    # API Urls
    url(r'^api/v1/', include('champions.api.urls')),
    url(r'^api/v1/', include('accounts.api.urls')),

    # Champions search, skins and champions
    url(r'^', include('champions.urls')),

    #This is to enable Fresh
    url(r'', include('fresh.urls')),
)
