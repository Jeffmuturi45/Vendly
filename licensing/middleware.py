class LicenseCheckMiddleware:
    """
    Phase 2: Will block access when a tenant's license has expired.
    For now this is a passthrough stub.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)