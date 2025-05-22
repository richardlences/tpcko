from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from accounts.models import UserProfile

from .models import Currency, UserCurrency

url = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_7PRJHGDL9xpzJW7AgjFohrVIhMWQvzmNimfCLY0A&currencies=EUR%2CUSD%2CGBP%2CCZK%2CCNY&base_currency=EUR"


@login_required
def index(request):
    currencies_list = Currency.objects.order_by("id")
    response = requests.get(url)
    data = response.json()["data"]
    for i in currencies_list:
        i.value = 1 / data[i.shortName]
        i.save()
    user_profile = request.user.userprofile
    user_currencies = {uc.currency_id: uc.amount for uc in user_profile.usercurrency_set.all()}
    context = {
        "currencies_list": currencies_list,
        "user_currencies": user_currencies,
    }
    return render(request, "assets/index.html", context)


@login_required
def detail(request, asset_id):
    currency = get_object_or_404(Currency, pk=asset_id)
    user_profile: UserProfile = request.user.userprofile
    user_currency = UserCurrency.objects.filter(user_profile=user_profile, currency=currency).first()
    owned_amount = user_currency.amount if user_currency else 0
    if request.method == "POST":
        action = request.POST.get("action")
        try:
            amount = float(request.POST.get("amount"))
        except (TypeError, ValueError):
            messages.error(request, "Invalid amount.")
            return redirect("detail", asset_id=asset_id)

        if action == "buy":
            total_cost = amount * currency.value
            if user_profile.account_balance >= total_cost:
                user_profile.account_balance -= total_cost
                user_profile.save()
                user_currency, created = UserCurrency.objects.get_or_create(
                    user_profile=user_profile,
                    currency=currency,
                    defaults={'amount': amount}
                )
                if not created:
                    user_currency.amount += amount
                    user_currency.save()
                messages.success(request, f"Successfully bought {amount} {currency.shortName}.")
            else:
                messages.error(request, "Insufficient balance.")
        elif action == "sell":
            if owned_amount >= amount:
                total_gain = amount * currency.value
                user_profile.account_balance += total_gain
                user_profile.save()
                user_currency.amount -= amount
                if user_currency.amount <= 0:
                    user_currency.delete()
                else:
                    user_currency.save()
                messages.success(request, f"Successfully sold {amount} {currency.shortName}.")
            else:
                messages.error(request, "You do not own enough to sell that amount.")


        return redirect("detail", asset_id=asset_id)
    context = {
        "currency": currency,
        "owned_amount": owned_amount,
        }
    return render(request, "assets/detail.html", context)
