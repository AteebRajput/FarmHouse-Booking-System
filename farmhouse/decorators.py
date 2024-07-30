from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'customer':
                return redirect('farm-list')
            if group == 'admin':
                return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapper_function
