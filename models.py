class Product:
    def __init__(self, name, base_price):
        self.name = name
        self.base_price = base_price

    def get_price(self):
        return self.base_price
    
class SeasonalProduct(Product):
    def __init__(self, name, base_price, season_discount):
        super().__init__(name, base_price)
        self.season_discount = season_discount

    def get_price(self):
        return self.base_price * (1 - self.season_discount)

class BulkProduct(Product):
    def __init__(self, name, base_price, bulk_quantity, bulk_discount):
        super().__init__(name, base_price)
        self.bulk_quantity = bulk_quantity
        self.bulk_discount = bulk_discount

    def get_price(self, quantity):
        if quantity >= self.bulk_quantity:
            return self.base_price * (1 - self.bulk_discount)
        return self.base_price

class Discount:
    def apply(self, price):
        return price

class PercentageDiscount(Discount):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply(self, price):
        return price * (1 - self.percentage)

class FixedAmountDiscount(Discount):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, price):
        return max(0, price - self.amount)

class Order:
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity, discount=None):
        price = product.get_price(quantity) if isinstance(product, BulkProduct) else product.get_price()
        if discount:
            price = discount.apply(price)
        self.items.append((product, quantity, price))

    def get_total(self):
        return sum(price for _, _, price in self.items)
