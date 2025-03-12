from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Currency


def index(request):
    currencies_list = Currency.objects.order_by("id")
    context = {"currencies_list": currencies_list}
    return render(request, "assets/index.html", context)


def detail(request, asset_id):
    currency = get_object_or_404(Currency, pk=asset_id)
    context = {"currency": currency}
    return render(request, "assets/detail.html", context)
