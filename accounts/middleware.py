from django.shortcuts import redirect

class CurrentTenantMiddleware:
    """
Attaches the tenant (Business) to every request.
Every queryset in views must filter by request.tenant.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant = None
        if request.user.is_authenticated and request.user.tenant_id:
            request.tenant = request.user.tenant
        return self.get_response(request)