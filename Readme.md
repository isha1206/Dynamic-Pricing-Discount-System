# Dynamic Pricing and Discount System

This project is a Flask-based API for managing products, applying discounts, and calculating order totals. The system uses object-oriented principles, including class inheritance and method overriding, to handle different types of products and discounts dynamically.

## Features

- **Product Management**: Create and manage different types of products (seasonal, bulk).
- **Discount Management**: Apply various discounts (percentage-based, fixed amount) to products.
- **Order Management**: Calculate the total price of an order considering product types and discounts.

## Technologies Used

- Python
- Flask
- Git for version control

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:


git clone https://github.com/isha1206/Dynamic-Pricing-Discount-System.git


### 2. Create a Virtual Environment
Create and activate a virtual environment:

python3 -m venv venv

- Activate the virtual environment:
- On macOS/Linux:
source venv/bin/activate
- On Wndows:
venv\Scripts\activate

### 3. Install Dependencies
Install the required dependencies:

pip install -r requirements.txt

### 4. Run the Application
Start the Flask application:

flask run

### 5. Test the API
Use a tool like Postman or curl to test the API. Example curl command to add an order:

curl -X POST http://127.0.0.1:5000/add_order \
-H "Content-Type: application/json" \
-d '{
    "items": [
        {
            "product_type": "seasonal",
            "name": "Winter Jacket",
            "base_price": 100,
            "quantity": 2,
            "season_discount": 0.20,
            "discount_type": "percentage",
            "percentage": 0.10
        },
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
}'

### 6. Running Tests
Run unit tests using pytest:

pytest
