from tastypie.authentication import SessionAuthentication,  \
                                    BasicAuthentication,    \
                                    MultiAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie import fields
from tastypie.resources import ModelResource

from accounts.models import Subscription

# Taken and modified from: http://django-tastypie.readthedocs.org/en/latest/authorization.html
class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        allowed = [x for x in object_list if x.user == bundle.request.user]
        return allowed

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        # Since they may not all be saved, iterate over them.
        allowed = [x for x in object_list if x.user == bundle.request.user]
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        allowed = [x for x in object_list if x.user == bundle.request.user]
        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

class SubscriptionResource(ModelResource):
    product = fields.ForeignKey('champions.api.resources.ProductResource', 'product')

    class Meta:
        queryset = Subscription.objects.all()
        resource_name = 'subscription'
        authentication = MultiAuthentication(SessionAuthentication(), BasicAuthentication())
        authorization = UserObjectsOnlyAuthorization()
        excludes = ['user']

    def obj_create(self, bundle, **kwargs):
        kwargs['user'] = bundle.request.user
        return super(SubscriptionResource, self).obj_create(bundle, **kwargs)
