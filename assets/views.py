from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import requests

from .models import Currency

url = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_7PRJHGDL9xpzJW7AgjFohrVIhMWQvzmNimfCLY0A&currencies=EUR%2CUSD%2CGBP%2CCZK%2CCNY&base_currency=EUR"


@login_required
def index(request):
    currencies_list = Currency.objects.order_by("id")
    response = requests.get(url)
    data = response.json()["data"]
    for i in currencies_list:
        i.value = 1 / data[i.shortName]
        i.save()
    context = {"currencies_list": currencies_list}
    return render(request, "assets/index.html", context)


@login_required
def detail(request, asset_id):
    currency = get_object_or_404(Currency, pk=asset_id)
    context = {"currency": currency}
    return render(request, "assets/detail.html", context)
