def current_tenant(request):
    """Injects the current tenant into every template context."""
    return {'current_tenant': getattr(request, 'tenant', None)}