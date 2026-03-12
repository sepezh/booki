""" context processor for pre defined variables """

from .forms import HomeSearchField


def search_field(request):
    """ Make visible search form available in all template """
    return {
        'search_field': HomeSearchField()
    }
