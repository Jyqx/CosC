rain_readings = [0.0, 0.0, 3.4, 33.8, 3.8, 0.0, 0.0, 0.0, 0.0, 0.0, 25.2, 12.2, 5.4, 0.4, 0.0, 0.0, 0.2, 0.0, 0.0, 1.6, 5.6, 25.8, 0.2, 0.0, 0.2, 0.4, 0.0, 0.2, 0.0, 15.6, 0.0, 0.0]

i = 0
total = 0
while i < len(rain_readings):
    total += rain_readings[i]
    i += 2

print(f"{total:.1f} mm of rain this month")