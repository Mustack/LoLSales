from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class SubscriptionView(TemplateView):

    template_name = 'subscriptions/subscription.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.request = request
        return super(SubscriptionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubscriptionView, self).get_context_data(**kwargs)

        user = self.request.user

        context['champions'] = user.champions

        return context
