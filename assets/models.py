from django.db import models


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=100)
    shortName = models.CharField(max_length=4)
    value = models.FloatField()
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name
