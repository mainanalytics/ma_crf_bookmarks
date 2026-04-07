class MainLogic:
    def __init__(self):

        self.default_value: int = 10

    def start_logic(self, input_value: int):
        result = self.prime_factors(n=input_value)

        # result = "11"
        # time.sleep(5)

        return result

    def prime_factors(self, n):
        factors = []

        # Handle factor 2 separately
        while n % 2 == 0:
            factors.append(2)
            n //= 2

        # Check odd numbers from 3 onwards
        i = 3
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            i += 2

        # If remaining n is a prime number > 2
        if n > 2:
            factors.append(n)

        # to str
        factor_str = " " + " ,".join([str(factor) for factor in factors])

        return factor_str
