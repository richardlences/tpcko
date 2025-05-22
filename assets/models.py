from django.db import models
from accounts.models import UserProfile


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=100)
    shortName = models.CharField(max_length=4)
    value = models.FloatField()
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class UserCurrency(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user_profile.user.username} - {self.currency.name} - {self.amount}'