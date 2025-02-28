"""
#		AUTHOR      :   Ayush Chinmay
#		DATE CREATED:   28 Feb 25
#		
#		DESCRIPTION : Implementation of Dual Numbers to perform forward automatic differentiation 
#                   > Ref: https://en.wikipedia.org/wiki/Dual_number
#		
"""
# ========== [ CLASS ] ========== #
class Dual:
    """ 
    Class to represent Dual Numbers
    -    Dual(a, b) = a + bε
    -    where ε is the infinitesimal number, defined by ε^2 = 0
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
        Representation of the Dual number
        :return: String representation of the Dual number
        """
        return f'Dual({self.real}, {self.dual})'
    
    def __str__(self):
        """
        String representation of the Dual number
        :return: String representation of the Dual number
        """
        return f'{round(self.real, 3)} {'+' if self.dual > 0 else '-'} {round(abs(self.dual), 3)}ε'
    
    def __eq__(self, other):
        """
        Equality check for Dual numbers
        :param other: Another Dual number
        :return: True if equal, False otherwise
        """
        if not isinstance(other, Dual):
            return False
        return self.real == other.real and self.dual == other.dual
    
    def __add__(self, other):
        """
        Addition of two Dual numbers
        :param other: Another Dual number
        :return: Result of the addition
        """
        if not isinstance(other, Dual):
            return Dual(self.real + other, self.dual)
        return Dual(self.real + other.real, self.dual + other.dual)
    
    def __sub__(self, other):
        """
        Subtraction of two Dual numbers
        :param other: Another Dual number
        :return: Result of the subtraction
        """
        if not isinstance(other, Dual):
            return Dual(self.real - other, self.dual)
        return Dual(self.real - other.real, self.dual - other.dual)
    
    def __mul__(self, other):
        """
        Multiplication of two Dual numbers
        :param other: Another Dual number
        :return: Result of the multiplication
        """
        if not isinstance(other, Dual):
            return Dual(self.real*other, self.dual*other)
        return Dual(self.real*other.real, self.real*other.dual + self.dual*other.real)
    
    def __truediv__(self, other):
        """
        Division of two Dual numbers
        :param other: Another Dual number
        :return: Result of the division
        """
        if not isinstance(other, Dual):
            return Dual(self.real/other, self.dual/other)
        return Dual(self.real/other.real, (self.dual*other.real - self.real*other.dual)/other.real**2)
    
    def __pow__(self, pow):
        """
        Power of a Dual number
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
        Conjugate of the Dual number
        :return: Conjugate of the Dual number
        """
        return Dual(self.real, -self.dual)


# ========== [ FUNCTIONS ] ========== #
def differentiate(func, x):
    """
    Differentiate a function at a point using Dual numbers
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
    print(f'b: {b}')
    
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