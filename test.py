import pytest
from flask import Flask, jsonify, request
from flask_testing import TestCase
from models import Product, SeasonalProduct, BulkProduct, PercentageDiscount, FixedAmountDiscount, Order

# Sample Flask app for testing
app = Flask(__name__)

@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.json
    order = Order()
    for item in data.get('items', []):
        product_type = item.get('product_type')
        name = item.get('name')
        base_price = item.get('base_price')
        quantity = item.get('quantity', 1)

        if product_type == 'seasonal':
            season_discount = item.get('season_discount', 0)
            product = SeasonalProduct(name, base_price, season_discount)
        elif product_type == 'bulk':
            bulk_quantity = item.get('bulk_quantity', 1)
            bulk_discount = item.get('bulk_discount', 0)
            product = BulkProduct(name, base_price, bulk_quantity, bulk_discount)
        else:
            product = Product(name, base_price)

        discount = None
        discount_type = item.get('discount_type')
        if discount_type == 'percentage':
            percentage = item.get('percentage', 0)
            discount = PercentageDiscount(percentage)
        elif discount_type == 'fixed_amount':
            amount = item.get('amount', 0)
            discount = FixedAmountDiscount(amount)

        order.add_product(product, quantity, discount)

    total_price = order.get_total()
    return jsonify({"total_price": total_price}), 200

class TestAddOrder(TestCase):
    def create_app(self):
        return app

    def test_add_order_seasonal_product(self):
        response = self.client.post('/add_order', json={
            "items": [
                {
                    "product_type": "seasonal",
                    "name": "Winter Jacket",
                    "base_price": 100,
                    "quantity": 2,
                    "season_discount": 0.20,
                    "discount_type": "percentage",
                    "percentage": 0.10
                }
            ]
        })
        data = response.json
        assert response.status_code == 200
        assert data['total_price'] == 160.0

    def test_add_order_bulk_product(self):
        response = self.client.post('/add_order', json={
            "items": [
                {
                    "product_type": "bulk",
                    "name": "Socks Pack",
                    "base_price": 10,
                    "quantity": 50,
                    "bulk_quantity": 10,
                    "bulk_discount": 0.15,
                    "discount_type": "fixed_amount",
                    "amount": 5
                }
            ]
        })
        data = response.json
        assert response.status_code == 200
        assert data['total_price'] == 425.0

    def test_add_order_multiple_products(self):
        response = self.client.post('/add_order', json={
            "items": [
                {
                    "product_type": "seasonal",
                    "name": "Winter Jacket",
                    "base_price": 100,
                    "quantity": 1,
                    "season_discount": 0.20,
                    "discount_type": "percentage",
                    "percentage": 0.10
                },
                {
                    "product_type": "bulk",
                    "name": "Socks Pack",
                    "base_price": 10,
                    "quantity": 20,
                    "bulk_quantity": 10,
                    "bulk_discount": 0.15,
                    "discount_type": "fixed_amount",
                    "amount": 5
                }
            ]
        })
        data = response.json
        assert response.status_code == 200
        assert data['total_price'] == 180.0

    def test_add_order_no_items(self):
        response = self.client.post('/add_order', json={})
        data = response.json
        assert response.status_code == 200
        assert data['total_price'] == 0.0

if __name__ == '__main__':
    pytest.main()
