from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from .models import Product, Champion, Skin
from django.http import Http404
from django.shortcuts import get_object_or_404

class ChampionView(TemplateView):

    template_name = "champions/champion.html"

    def get_context_data(self, **kwargs):
        context = super(ChampionView, self).get_context_data(**kwargs)
        return context

class SkinView(TemplateView):

    template_name = "champions/skin.html"

    def get_context_data(self, **kwargs):
        context = super(SkinView, self).get_context_data(**kwargs)
        return context

class ProductView(RedirectView):
    permanent = False

    def get_redirect_url(self, slug):
        product = get_object_or_404(Product, slug=slug)
        try:
            skin = product.skin
            return skin.get_absolute_url()
        except Skin.DoesNotExist:
            pass

        try:
            champion = product.champion
            return champion.get_absolute_url()
        except Champion.DoesNotExist:
            pass

        raise Exception('Unable to find skin or champion for product')

class SearchView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self):
        product = self.request.GET['product']
        try:
            product = Product.objects.get_subclass(pk=product)
            return product.get_absolute_url()
        except Product.DoesNotExist:
            raise Http404
