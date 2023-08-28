def num_rushes(slope_height, rush_height_gain, back_sliding):
    """Herbert the Heffalump"""
    current_height = 0
    rushes = 0
    first_rush = True
    while current_height < slope_height:
        if first_rush == True:
            current_height += rush_height_gain
            first_rush = False
            if current_height < slope_height:
                current_height -= back_sliding 
        else:
            current_height += rush_height_gain * 0.95 ** rushes
            if current_height < slope_height:
                current_height -= back_sliding * 0.95 ** rushes
        rushes += 1
    return rushes
# UC solution
# def num_rushes(slope_height, rush_height_gain, back_sliding):
#     """Herbert the Heffalump"""
#     current_height = 0
#     rushes = 0
#     while current_height < slope_height:
#         current_height += rush_height_gain
#         if current_height < slope_height:
#             current_height -= back_sliding
#         rush_height_gain *= 0.95
#         back_sliding *= 0.95
#         rushes += 1
#     return rushes

ans = num_rushes(100, 15, 7)
print(ans)