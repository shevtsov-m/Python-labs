def myfunction(name, quantity, action):
    if action == "add":
        if name in products:
            products[name] += quantity
        else:
            products[name] = quantity
    elif action == "remove":
        products[name] -= quantity
        if products[name] < 0:
            products[name] = 0


products = {"apple": 10,
            "cheese": 5,
            "banana": 7,
            "orange": 6,
            "bread": 4}

myfunction("apple", 7, "remove")
myfunction("bread", 5, "add")
myfunction("orange", 4, "remove")


less = []

for name in products:
    if products[name] < 5:
        less.append(name)

print("products and their quantity are: ", products)
print("products with quantity less then 5 are: ", less)