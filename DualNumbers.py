"""
#		AUTHOR      :   Ayush Chinmay
#		DATE CREATED:   28 Feb 25
#		
#		DESCRIPTION : Implementation of Dual Numbers to perform automatic differentiation of polynomials
#
#       REFERENCES
#           -   Computerphile -- [Finding The Slope Algorithm](https://www.youtube.com/watch?v=QwFLA5TrviI)
#           -   Wikipedia -- [Dual Number](https://en.wikipedia.org/wiki/Dual_number)
#		
"""
# ========== [ CLASS ] ========== #
class Dual:
    """ 
    Class to represent Dual Numbers
    -    Dual(a, b) = a + bε
    -    where ε is the infinitesimal number, defined by ε^2 = 0

    Attributes:
    - real: Real part of the dual number    [a]
    - dual: Dual part of the dual number    [ε]
    """
    __slots__ = ('real', 'dual')

    def __init__(self, real: float, dual: float):
        """
        Constructor for Dual class
        :param real: Real part of the dual number
        :param dual: Dual part of the dual number
        """
        self.real = real
        self.dual = dual

    def __repr__(self):
        """
        Representation of the Dual number : `Dual(a, b)`
        :return: String representation of the Dual number
        """
        return f'Dual({self.real}, {self.dual})'
    
    def __str__(self):
        """
        String representation of the Dual number : `a + bε`
        [Note]      - ε is represented by the symbol 'ε'
                    - Edit the precision of the output by modifying the variable `precision` 
        :return: String representation of the Dual number
        """
        precision = 3   # <MODIFY> Configure precision of the output
        if self.dual == 0:
            return f'{round(self.real, precision)}'
        return f'{round(self.real, precision)} {'+' if self.dual > 0 else '-'} {round(abs(self.dual), precision)}ε'
    
    def __eq__(self, other):
        """
        Equality check for Dual numbers : `(a + bε) == (c + dε) <=> a == c and b == d`
        :param other: Another Dual number
        :return: True if equal, False otherwise
        """
        if not isinstance(other, Dual):
            return False
        return self.real == other.real and self.dual == other.dual
    
    def __add__(self, other):
        """
        Addition of two Dual numbers : `(a + bε) + (c + dε) = (a + c) + (b + d)ε`
        :param other: Another Dual number
        :return: Result of the addition
        """
        if not isinstance(other, Dual):
            return Dual(self.real + other, self.dual)
        return Dual(self.real + other.real, self.dual + other.dual)
    
    def __sub__(self, other):
        """
        Subtraction of two Dual numbers : `(a + bε) - (c + dε) = (a - c) + (b - d)ε`
        :param other: Another Dual number
        :return: Result of the subtraction
        """
        if not isinstance(other, Dual):
            return Dual(self.real - other, self.dual)
        return Dual(self.real - other.real, self.dual - other.dual)
    
    def __mul__(self, other):
        """
        Multiplication of two Dual numbers : `(a + bε)(c + dε) = ac + (ad + bc)ε`
        :param other: Another Dual number
        :return: Result of the multiplication
        """
        if not isinstance(other, Dual):
            return Dual(self.real*other, self.dual*other)
        return Dual(self.real*other.real, self.real*other.dual + self.dual*other.real)
    
    def __truediv__(self, other):
        """
        Division of two Dual numbers : `(a + bε)/(c + dε) = (a*c + b*d)/(c**2) + ((b*c - a*d)/(c**2))ε`
        :param other: Another Dual number
        :return: Result of the division
        """
        if not isinstance(other, Dual):
            return Dual(self.real/other, self.dual/other)
        if other.real == 0:
            raise ZeroDivisionError('Division by zero')
        return Dual(self.real/other.real, (self.dual*other.real - self.real*other.dual)/other.real**2)
    
    def __pow__(self, pow):
        """
        Power of a Dual number : `(a + bε)**pow = a**pow + pow*a**(pow-1)*bε`
        :param pow: Power to raise the Dual number to
        :return: Result of the power
        """
        if not isinstance(pow, int):
            raise ValueError('Power must be an integer')
        if pow == 0:
            return Dual(1, 0)
        return Dual(self.real**pow, pow*self.real**(pow-1)*self.dual)
    
    def conjugate(self):
        """
        Conjugate of the Dual number : `(a + bε).conjugate() = a - bε`
        :return: Conjugate of the Dual number
        """
        if self.dual == 0:
            return Dual(self.real, 0)
        return Dual(self.real, -self.dual)


# ========== [ FUNCTIONS ] ========== #
def differentiate(func, x):
    """
    Differentiate a function at a point using Dual numbers
        f'(x) = f(x + ε) - f(x) / ε
    :param func: Function to differentiate
    :param x: Point to differentiate at
    :return: Derivative of the function at the point
    """
    return func(Dual(x, 1)).dual


# ========== [ DEBUG ] ========== #
def debug_main():
    """
    Debugging function to test the Dual class and differentiation
    """
    # Test Dual Numbers
    a = Dual(1, 2)
    b = Dual(3, 4)
    
    print(f'a: {a}')
    print(f'~b: {b.conjugate()}')
    
    print(f'a + b: {a + b}')
    print(f'a - b: {a - b}')
    print(f'a * b: {a * b}')
    print(f'a / b: {a / b}')
    
    # Test Differentiation
    def f(x):
        return x**2 + x*2 + 1
    
    print(f'Derivative of f at x=1: {differentiate(f, 18)}')


if __name__ == '__main__':
    debug_main()
