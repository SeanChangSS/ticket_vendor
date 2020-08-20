import os
import json
from http import HTTPStatus

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import TransactionRecord

# Create your views here.

def index(request):
    return render(request, 'change_money/index.html', {})

def buy_ticket(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        _purchase_info = {
            "amount": data["amount"],
            "ticket_price": data["ticket_price"],
            "money_paid": data["money_paid"],
        }
        exchange, total_price = _exchanging(_purchase_info)
        if exchange >= 0:
            transaction_record = TransactionRecord(price=total_price, amount=_purchase_info["amount"])
            return JsonResponse({'data': {'exchange': exchange}}, status=HTTPStatus.OK)
        else:
            return JsonResponse({'message': '請投入足夠金額。'}, status=HTTPStatus.BAD_REQUEST)
        pass
    return JsonResponse({}, status=HTTPStatus.BAD_REQUEST)

def _exchanging(purchase_info):
    total_price = purchase_info["amount"] * purchase_info["ticket_price"]
    exchange = purchase_info["money_paid"] - total_price
    return exchange, total_price


