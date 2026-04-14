# accounts/decorators.py
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # If user is admin/superuser, they have access to everything
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # If they try to access a page not for their role, send them to their dashboard
                if request.user.role == 'STUDENT': return redirect('student_dashboard')
                if request.user.role == 'FACULTY': return redirect('faculty_dashboard')
                if request.user.role == 'COUNSELOR': return redirect('counselor_dashboard')
                raise PermissionDenied 
        return wrapper_func
    return decorator