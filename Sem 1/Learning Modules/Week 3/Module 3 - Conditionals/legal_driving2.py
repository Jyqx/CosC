"""
Program to determine if a person is allowed to drive, given their
age and blood alcohol level.
"""

def main():
    """Main Program"""
    alcohol_level = float(input("Enter blood alcohol level (mg/100ml): "))
    age = float(input("Enter age in years: "))
    if (age < 20 and alcohol_level > 0) or alcohol_level >= 50:
        print("You're not allowed to drive")
    elif (age <= 20 and 30 <= alcohol_level <= 50):
        print("You're legally allowed to drive, but please don't")
    else:
        print("You're allowed to drive")

main()