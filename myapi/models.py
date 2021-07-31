from django.db import models
from datetime import date

# Create your models here.
class Hero(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class Claims(models.Model):
    name = models.CharField(max_length=60)
    age = models.IntegerField(max_length=3)
    address = models.CharField(max_length=60)
    license_num = models.CharField(max_length=60)
    id_proof = models.CharField(max_length=60)
    claims_amount = models.IntegerField(default=0)
    created_date = models.DateField(date.today())

    