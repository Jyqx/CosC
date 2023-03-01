
# Attempt 1
# def discount_price(discount_amount, price):
#     """
#     Calculates discounts.
#     """
#     discounted_price = (discount_amount * price) / 100
#     price = (price-discounted_price)
#     return price

# def dinner_calculator(meal_cost, drinks_cost):
#     """
#     Calculates cost of dinner.
#     """
#     drinks = discount_price(30, drinks_cost)
#     meal_cost = drinks + meal_cost
#     total_cost = discount_price(15, meal_cost)
#     return total_cost

#  Attempt 2
# def dinner_calculator(meal_cost, drinks_cost):
#     """
#     Calculates cost of dinner.
#     """
#     discounted_drinks = (30 * drinks_cost) / 100
#     drinks_price = (drinks_cost-discounted_drinks)
#     meal_cost = drinks_price + meal_cost
#     discounted_meal = (15 * meal_cost) / 100
#     total_cost = meal_cost - discounted_meal
#     return total_cost

# #Attempt 3
# def dinner_calculator(meal_cost, drinks_cost):
#     """
#     Calculates cost of dinner.
#     """
#     discounted_drinks = (drinks_cost * 0.7)
#     total_meal = discounted_drinks + meal_cost
#     discounted_meal = (total_meal * 1.15)
#     return discounted_meal

#Chat GPT Attempt
def dinner_calculator(meal_cost, drinks_cost):
    """
    Calculates cost of dinner.
    """
    discounted_drinks_cost = 0.7 * drinks_cost
    subtotal = meal_cost + discounted_drinks_cost
    tax = 0.15 * subtotal
    total_cost = subtotal + tax
    return total_cost
