from django import forms

class PurchaseForm(forms.Form):
    ticket_amount = forms.IntegerField(label='ticket_amount')
    money_paid = forms.IntegerField(label='paid_money')