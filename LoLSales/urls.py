from django.conf.urls import patterns, include, url

from django.contrib import admin
from djrill import DjrillAdminSite

from champions import views

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
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^champion/', 'champions.views.get_champion'),
)
