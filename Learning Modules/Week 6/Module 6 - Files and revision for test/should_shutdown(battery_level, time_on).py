def should_shutdown(battery_level, time_on):
    """
    Check logic for battery level and time_on
    """
    if time_on >= 60 and battery_level < 4.8:
        return True
    elif time_on < 60 and battery_level < 4.7:
        return True
    else:
        return False
    
ans = should_shutdown(5, 10)
print(ans)
ans = should_shutdown(4.74, 90)
print(ans)
ans = should_shutdown(4.74, 50)
print(ans)
