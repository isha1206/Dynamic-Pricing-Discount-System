from flask import Flask, jsonify, request
from models import Product, SeasonalProduct, BulkProduct, PercentageDiscount, FixedAmountDiscount, Order

app = Flask(__name__)

@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.json
    
    # Create an Order instance
    order = Order()
    
    # Loop through the items in the request
    for item in data.get('items', []):
        # Extract product details
        product_type = item.get('product_type')
        name = item.get('name')
        base_price = item.get('base_price')
        quantity = item.get('quantity', 1)
        
        # Initialize the product object based on its type
        if product_type == 'seasonal':
            season_discount = item.get('season_discount', 0)
            product = SeasonalProduct(name, base_price, season_discount)
        elif product_type == 'bulk':
            bulk_quantity = item.get('bulk_quantity', 1)
            bulk_discount = item.get('bulk_discount', 0)
            product = BulkProduct(name, base_price, bulk_quantity, bulk_discount)
        else:
            product = Product(name, base_price)
        
        # Initialize the discount object if provided
        discount = None
        discount_type = item.get('discount_type')
        if discount_type == 'percentage':
            percentage = item.get('percentage', 0)
            discount = PercentageDiscount(percentage)
        elif discount_type == 'fixed_amount':
            amount = item.get('amount', 0)
            discount = FixedAmountDiscount(amount)
        
        # Add the product to the order
        order.add_product(product, quantity, discount)
    
    # Calculate the total price
    total_price = order.get_total()
    
    return jsonify({"total_price": total_price}), 200

if __name__ == '__main__':
    app.run(debug=True)
