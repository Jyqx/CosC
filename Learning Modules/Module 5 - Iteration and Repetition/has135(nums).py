def has135(nums):
    """check for 135"""
    for i in range(len(nums) - 2):
        if nums[i] == 1 and nums[i+1] == 3 and nums[i+2] == 5:
            return True
    return False


print(has135([1, 1, 3, 5, 1]))