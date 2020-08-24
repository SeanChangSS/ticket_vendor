import os
import json
import logging
from http import HTTPStatus

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from .models import TransactionRecord
from .forms import PurchaseForm

# Create your views here.


def index(request):
    return render(request, 'change_money/index.html', {})


def buy_ticket(request):
    denomination_list = [1000, 500, 100, 50, 10, 5, 1]

    if request.method == 'POST':
        purchase_form = PurchaseForm(request.POST)
        if purchase_form:
            _purchase_info = {
                "ticket_amount": purchase_form.data["ticket_amount"],
                "ticket_price": 20,
                "money_paid": purchase_form.data["money_paid"],
                "denomination_list": denomination_list
            }
            exchange, total_price = _exchanging(_purchase_info)
            if exchange is None:
                return render(request, 'change_money/index.html', {"alert": "Something goes wrong."})
            elif total_price is None:
                return render(request, 'change_money/index.html', {"alert": "Please insert enough money."})
            else:
                print('Ticket has purchased successfully.')
                try:
                    transaction_record = TransactionRecord(price=total_price, amount=_purchase_info["ticket_amount"])
                    transaction_record.save()
                except Exception:
                    logging.exception(Exception)
                    return render(request, 'change_money/index.html', {"alert": "Something goes wrong."})

                return render(request, 'change_money/index.html', {"alert": "Your exchange is: {}".format(exchange)})

    return render(request, 'change_money/index.html', {"alert": "Something goes wrong."})


def _exchanging(purchase_info):
    # TODO
    # Exchange with NTD denomination
    try:
        ticket_amount = _to_integer(purchase_info["ticket_amount"])
        money_paid = _to_integer(purchase_info["money_paid"])
        ticket_price = _to_integer(purchase_info["ticket_price"])
        denomination_list = purchase_info["denomination_list"]

    except TypeError:
        logging.exception(TypeError)
        return None, None

    except Exception:
        logging.exception(Exception)
        return None, None

    total_price = ticket_amount * ticket_price
    exchange = money_paid - total_price
    exchange_dict = {}
    if exchange >= 0:
        for denomination in denomination_list:
            exchange_dict.update({denomination: exchange//denomination})
            exchange = exchange % denomination
        return exchange_dict, total_price
    else:
        return exchange, None

    return None, None


def _to_integer(e):
    if isinstance(e, int) and not isinstance(e, bool):
        if e > 0:
            return e
        raise TypeError('Please insert positive integer.')
    elif isinstance(e, str):
        if e.isdecimal():
            return int(e)
        raise TypeError('Please insert positive integer.')
    raise TypeError('Please insert positive integer.')
