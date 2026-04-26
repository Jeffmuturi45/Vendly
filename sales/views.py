from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def pos_view(request):
    return render(request, 'sales/pos.html')

@login_required
def list_view(request):
    return render(request, 'sales/list.html')

@login_required
def detail_view(request, pk):
    return render(request, 'sales/detail.html', {'pk': pk})