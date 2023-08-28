def total_cost(kilograms, litres, discount_proportion):
    """
    Function used to calculate total discounted cost then
    apply the GST tax.
    """
    nails_cost = kilograms * 5
    paint_cost = litres * 10
    added_cost = (nails_cost + paint_cost)
    discount = added_cost * discount_proportion
    discounted_cost = added_cost - discount
    item_cost = discounted_cost * 1.15
    return item_cost
    