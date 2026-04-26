from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from tenants.models import Business
from accounts.models import CustomUser


def superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            from django.shortcuts import redirect
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@superadmin_required
def dashboard(request):
    businesses = Business.objects.all().order_by('-created_at')
    users      = CustomUser.objects.all()
    context = {
        'total_businesses': businesses.count(),
        'total_users':      users.count(),
        'active_businesses':businesses.filter(is_active=True).count(),
        'recent_businesses':businesses[:8],
        'today':            timezone.now(),
    }
    return render(request, 'superadmin/dashboard.html', context)


@superadmin_required
def businesses(request):
    businesses = Business.objects.all().order_by('-created_at')
    return render(request, 'superadmin/businesses.html',
                  {'businesses': businesses})


@superadmin_required
def users(request):
    users = CustomUser.objects.select_related('tenant').order_by('-date_joined')
    return render(request, 'superadmin/users.html', {'users': users})


@superadmin_required
def licenses(request):
    businesses = Business.objects.all()
    return render(request, 'superadmin/licenses.html',
                  {'businesses': businesses})