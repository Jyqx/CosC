def num_doublings(initial_population, final_population):
    """Check how many days it takes for init to reach final"""
    day = 0
    population = initial_population
    while population <= final_population:
        if population >= final_population:
            return day
        population *= 2
        day += 1
    if population >= final_population:
        return day

ans = num_doublings(9, 8)
print(ans)
