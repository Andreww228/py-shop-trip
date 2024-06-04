import json
import os

from app.car import Car
from app.customer import Customer
from app.shop import Shop


def shop_trip() -> None:
    data = {}
    directory = os.path.dirname(os.path.abspath(__file__))
    with open(f"{directory}/config.json", "r") as config:
        data = json.load(config)

    # Initialize data from dict
    fuel_price = data["FUEL_PRICE"]
    customers = []
    shops = []

    for customer in data["customers"]:
        customers.append(Customer(
            customer["name"],
            customer["product_cart"],
            customer["location"],
            customer["money"],
            Car(
                customer["car"]["brand"],
                customer["car"]["fuel_consumption"]
            )
        ))

    for shop in data["shops"]:
        shops.append(Shop(
            shop["name"],
            shop["location"],
            shop["products"]
        ))

    for customer_index, customer in enumerate(customers):
        print(f"{customer.name} has {customer.money} dollars")

        cheapest_shop = None
        cheapest_trip_cost = 0.0
        for shop in shops:
            trip_cost = (
                ((customer.calculate_distance(shop.location) / 100)
                 * customer.car.fuel_consumption) * fuel_price
            ) * 2

            for product, amount in customer.product_cart.items():
                if product in shop.products:
                    total_product_cost = shop.products[product] * amount
                    trip_cost += total_product_cost
                else:
                    continue

            if not cheapest_shop or cheapest_trip_cost > trip_cost:
                cheapest_shop = shop
                cheapest_trip_cost = trip_cost

            trip_cost = round(trip_cost, 2)
            print(f"{customer.name}'s trip to the "
                  f"{shop.name} costs {trip_cost}")

        if not cheapest_shop or cheapest_trip_cost > customer.money:
            print(f"{customer.name} doesn't have "
                  f"enough money to make a purchase in any shop")
            if customer_index != len(customers) - 1:
                print("")
            continue

        customer_location = customer.location
        print(f"{customer.name} rides to {cheapest_shop.name}\n")
        customer.location = cheapest_shop.location
        cheapest_shop.serve_customer(customer)
        print(f"{customer.name} rides home")
        customer.location = customer_location
        customer.money -= cheapest_trip_cost
        print(f"{customer.name} now has {round(customer.money, 2)} dollars\n")


shop_trip()
