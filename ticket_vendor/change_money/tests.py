import copy
import unittest
from django.test import TestCase

from .views import _exchanging

# Create your tests here.


def simple_purchase(ticket_amount, ticket_price, money_paid):
    return _exchanging({
        "ticket_amount": ticket_amount,
        "ticket_price": ticket_price,
        "money_paid": money_paid,
        "denomination_list": [1000, 500, 100, 50, 10, 5, 1]
    })


class TestExchange(TestCase):

    def _test_input(self):

        exchange, total_amount = simple_purchase(3, 25, 80)
        self.assertEqual(exchange, 5)

        exchange, total_amount = simple_purchase(2, 70, 80)
        self.assertEqual(exchange, -60)

        exchange, total_amount = simple_purchase(9, 53, 689)
        self.assertEqual(exchange, 212)

        exchange, total_amount = simple_purchase('ds', 25, 80)
        self.assertIsNone(exchange)

        exchange, total_amount = simple_purchase(1, 25, 0x24)
        self.assertEqual(exchange, 11)

        exchange, total_amount = simple_purchase(-4, 25, 100)
        self.assertIsNone(exchange)

        exchange, total_amount = simple_purchase(5.4, 25, 150)
        self.assertIsNone(exchange)

        exchange, total_amount = simple_purchase(9, 33.2, 500)
        self.assertIsNone(exchange)

        exchange, total_amount = simple_purchase(2, 10, 30.2)
        self.assertIsNone(exchange)

    def test_exchange(self):

        exchange, total_amount = simple_purchase(1, 25, 80)
        self.assertEqual(exchange, [0, 0, 0, 1, 0, 1, 0])

        exchange, total_amount = simple_purchase(5, 35, 10)
        self.assertTrue(exchange < 0)

        exchange, total_amount = simple_purchase("10", 10, 200)
        self.assertEqual(exchange, [0, 0, 1, 0, 0, 0, 0])

        exchange, total_amount = simple_purchase("20", "20", "400")
        self.assertEqual(exchange, 0)

        exchange, total_amount = simple_purchase(-3, 25, 200)
        self.assertIsNone(exchange)

        exchange, total_amount = simple_purchase(5.4, 25, 150)
        self.assertIsNone(exchange)

        exchange, total_amount = simple_purchase(9, 33.2, 500)
        self.assertIsNone(exchange)

        exchange, total_amount = simple_purchase(2, 10, 30.2)
        self.assertIsNone(exchange)

        exchange, total_amount = simple_purchase(5.4, 25, 150)
        self.assertIsNone(exchange)

        exchange, total_amount = simple_purchase(9, 33.2, 500)
        self.assertIsNone(exchange)

        exchange, total_amount = simple_purchase(2, -10, 30.2)
        self.assertIsNone(exchange)
