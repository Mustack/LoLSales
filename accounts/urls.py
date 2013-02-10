from django.conf.urls import patterns, url
from .views import SubscriptionView

urlpatterns = patterns('',
	url(r'^subscriptions/', SubscriptionView.as_view())
)