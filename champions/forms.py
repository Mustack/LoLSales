from django import forms
from .models import Product
import autocomplete_light


class ProductSearchForm(forms.Form):
    product = forms.ModelChoiceField(Product.objects.all(),
        widget=autocomplete_light.ChoiceWidget('ProductAutocomplete',
        autocomplete_js_attributes={'minimum_characters': 1,
                                    'placeholder': 'Find a Champion or Skin...'}))
