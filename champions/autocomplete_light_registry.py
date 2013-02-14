from .models import Product
import autocomplete_light

autocomplete_light.register(Product, search_fields=('name',), name='ProductAutocomplete')
