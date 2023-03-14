def fire_risk(temperature, rainless_days):
    """Check if day is humid and take temperature"""
    if (rainless_days < 28 and temperature < 25):
        return "Low"
    elif (rainless_days < 28 and temperature >= 25) or (rainless_days >= 28 and temperature < 25):
        return "Medium"
    else:
        return "High"
    