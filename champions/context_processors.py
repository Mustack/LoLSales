from .forms import ProductSearchForm

def add_search_form(request):
    return {'search_form': ProductSearchForm()}
