""" Custom decorators """
from functools import wraps
from django.shortcuts import redirect


def redirect_login_user(redirect_url='home'):
    """ Redirect if user is login """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def ajax_required(view_func):
    """ Redirect home if request is not ajax """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        is_fetch = request.headers.get('accept') == 'application/json' or request.content_type == 'application/json'
        if not (is_ajax or is_fetch):
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def librarian_required(view_func):
    """ Check user is a librarian """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_authenticated or request.user.groups.filter(name='librarian').exists()):
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
