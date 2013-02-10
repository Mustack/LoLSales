from django.conf.urls import patterns, url


urlpatterns = patterns('',
	url(r'^subscriptions/', 'accounts.subscriptionsview.get')
)