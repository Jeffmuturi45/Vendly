from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    error = False
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return _redirect_by_role(user)
        error = True
        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html', {'error': error})


def _redirect_by_role(user):
    if user.is_superuser:
        return redirect('superadmin:dashboard')
    if user.tenant_id:
        return redirect('dashboard:home')
    # staff user with no tenant — send back to login with message
    return redirect('accounts:login')


def logout_view(request):
    logout(request)
    return redirect('landing:index')


def register_view(request):
    return redirect('tenants:onboarding')