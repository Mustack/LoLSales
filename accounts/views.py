from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views.generic import TemplateView


class SubscriptionView(TemplateView):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello World!')
