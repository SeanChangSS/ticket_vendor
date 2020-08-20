from django.urls import path

from .views import index, buy_ticket

urlpatterns = [
    path('', index, name='index'),
    path('ticket/buy/', buy_ticket, name="buy_ticket"),
]