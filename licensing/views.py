from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def status(request):
    return render(request, 'licensing/status.html')