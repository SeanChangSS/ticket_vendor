from django.db import models

# Create your models here.

class TransactionRecord(models.Model):
    price = models.IntegerField(verbose_name="總金額")
    amount = models.IntegerField(verbose_name="票卷張數")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="購買日期與時間")