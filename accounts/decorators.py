# accounts/decorators.py
from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden

#un decorator pour s'assurer que les pages utilisent les roles exacts
def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role != roles:
                return HttpResponseForbidden("Accès interdit")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
