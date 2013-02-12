from django.conf.urls.defaults import url, patterns, include
from .resources import SubscriptionResource

subscription_resource = SubscriptionResource()

urlpatterns = patterns('',
    url(r'^', include(subscription_resource.urls))
)
