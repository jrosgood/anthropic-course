def greeting():
    print("Hello, world!")


def calculate_pi_fifth_digit():
    """
    Calculate pi to the 5th digit using the Machin formula.
    Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    
    Returns the value of pi rounded to 5 decimal places.
    """
    from decimal import Decimal, getcontext
    
    # Set precision high enough to calculate 5 decimal places accurately
    getcontext().prec = 50
    
    # Calculate arctan using Taylor series
    def arctan(x, num_terms=100):
        x = Decimal(x)
        power = x
        result = power
        for n in range(1, num_terms):
            power *= -x * x
            result += power / (2 * n + 1)
        return result
    
    # Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    pi = 4 * (4 * arctan(Decimal(1) / Decimal(5)) - arctan(Decimal(1) / Decimal(239)))
    
    # Round to 5 decimal places
    return float(round(pi, 5))