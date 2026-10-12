sales = [
    {"product": "Laptop", "quantity": 2, "price": 25000},
    {"product": "Mouse", "quantity": 5, "price": 500},
    {"product": "Laptop", "quantity": 1, "price": 25000},
    {"product": "Keyboard", "quantity": 3, "price": 1500},
    {"product": "Mouse", "quantity": 4, "price": 500}
]

def calculate_revenue():
    revenue = {}

    for sale in sales:
        income = sale["quantity"] * sale["price"]

        if sale["product"] in revenue:
            revenue[sale["product"]] += income
        else:
            revenue[sale["product"]] = income

    return revenue


def calculate_more_than_1000():
    more_than_1000 = []

    for product in revenue:
        if revenue[product] > 1000:
            more_than_1000.append(product)

    return more_than_1000

revenue = calculate_revenue()

print("Revenue:", revenue)
print("Products with revenue greater than 1000:", calculate_more_than_1000())