def num_rushes(slope_height, rush_height_gain, back_sliding):
    """Calculates the number of rushes needed for Herbert the Heffalump to climb the slope."""
    current_height = 0
    rushes = 0
    top = False
    while current_height < slope_height and top == False:
        current_height += rush_height_gain
        if current_height >= slope_height:
            rushes +=1
            top = True
        else:
            current_height -= back_sliding
            rushes += 1
    return rushes

# UC Answer
# def num_rushes(slope_height, rush_height_gain, back_sliding):
#     """Herbert the Heffalump"""
#     current_height = 0
#     rushes = 0
#     while current_height < slope_height:
#         current_height += rush_height_gain
#         if current_height < slope_height:
#             current_height -= back_sliding
#         rushes += 1
#     return rushes

ans = num_rushes(100, 10, 0)
print(ans)