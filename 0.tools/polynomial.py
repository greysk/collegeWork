import numbers

from enum import Enum
from fractions import Fraction
from math import sqrt
import re


def convert_to_int(n: float | Fraction) -> int | Fraction:
    """Convert float of fraction to int when value represent an int.

    >>> convert_to_int(0.5)
    Fraction(1, 2)
    >>> convert_to_int(1.0)
    1
    >>> convert_to_int(Fraction('2/1'))
    2
    """
    if n == 0:
        n = 0
    elif isinstance(n, Fraction) and n.denominator == 1:
        n = n.numerator
    elif isinstance(n, float):
        if n - int(n) == 0:
            n = int(n)
        else:
            n = Fraction(n)
    return n


def convert_to_numeric(s: str) -> int | Fraction:
    if '.' in s or '/' in s:
        n = Fraction(s)
    else:
        n = int(s)
    return convert_to_int(n)


def get_factors(n: int) -> list:
    """Returns the factors of a given integer.

    >>> get_factors(2)
    [1, 2]
    >>> get_factors(12)
    [1, 2, 3, 4, 6, 12]
    """
    if n == 0:
        return [0]
    n = abs(n)
    return [i for i in range(1, n+1) if n % i == 0]


def quadratic_formula(coefficients: list) -> tuple:
    """Obtain parts of resulting quadratic formula.

    Returns:
        (tuple): (str) value before determinate over 2(a),
                 (str) determinate over 2(a)
    """
    if len(coefficients) != 3:
        raise ValueError(
            'The quadratic formula can only be used on a 3-degree polynomial.')
    A = coefficients[0]
    B = coefficients[1]
    C = coefficients[2]

    determinate = pow(B, 2) - (4 * A * C)
    denominator = 2 * A
    k = Fraction(-B, denominator)

    if determinate < 0:
        i = 'i'
    else:
        i = ''

    sqrt_determinate = sqrt(abs(determinate))
    if sqrt_determinate - int(sqrt_determinate) == 0:
        m = f'{Fraction(int(sqrt_determinate), denominator)}{i}'
    else:
        m = f'{i}√({sqrt_determinate})/{denominator}'
    return k, m, denominator


class XDEGREE(bytes, Enum):
    def __new__(cls, value: int, unicode: str):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.pwr = unicode
        return obj

    ONE = (1, chr(185))
    TWO = (2, chr(178))
    THREE = (3, chr(179))
    FOUR = (4, chr(8308))
    FIVE = (5, chr(8309))
    SIX = (6, chr(8310))
    SEVEN = (7, chr(8311))
    EIGHT = (8, chr(8312))
    NINE = (9, chr(8313))

    @staticmethod
    def powers() -> dict:
        return {XDEGREE(n).pwr: XDEGREE(n).value for n in range(1, 10)}


class Term:
    def __init__(self, coefficient: numbers, variable: str = '',
                 degree: numbers = 0) -> None:
        """Constructor. `Term` represents a polynomial term.

        Args:
            `coefficient` (numbers): The term coefficient.
            `variable` (str, optional): The term variable. Defaults to 'x'.
            `degree` (numbers): The degree/power of the variable for the term
        """
        self.coeff = coefficient
        self.variable = variable
        self.degree = degree
        if isinstance(degree,  XDEGREE):
            self.degree = XDEGREE(degree).value
        self._parts = [self.coeff, self.variable, self.degree]

        if self.degree == 0 or self.coeff == 0:
            self._term = str(self.coeff)
        else:
            coeff = Term.str_coeff(self.coeff)
            powered_var = Term.str_powered_var(self.variable,
                                               self.degree)
            self._term = f'{coeff}{powered_var}'

    def __repr__(self) -> str:
        if self.degree == 0:
            return f'Term({self.coeff})'
        return (
            f"Term({self.coeff}, '{self.variable}', {self.degree})")

    def __str__(self) -> str:
        """
        Return the string version of the term.

        Returns:
            str: The string version of the term.

        >>> term = Term(1, 'x', 2)
        >>> str(term)
        'x²'
        >>> term = Term(2, 'x', 2)
        >>> str(term)
        '2x²'
        >>> term = Term(1, 'x', 1)
        >>> str(term)
        'x'
        >>> term = Term(2, 'x', 1)
        >>> str(term)
        '2x'
        >>> term = Term(0)
        >>> str(term)
        '0'
        """
        return self._term

    def __contains__(self):
        return self.parts

    def __len__(self):
        return(len(self.parts))

    @staticmethod
    def str_coeff(coefficient: numbers) -> str:
        """Convert a number to a string as displayed with a variable in a term.

        Args:
            `coefficient` (numbers): The coefficient.

        Returns:
            `str`: If the term coefficient is 1 or 0, return an empty string.
                   Otherwise, return the coefficient as a string.

        >>> Term.str_coeff(1)
        ''
        >>> Term.str_coeff(0)
        ''
        >>> Term.str_coeff(2)
        '2'
        >>> Term.str_coeff(0.5)
        '1/2'
        """
        if coefficient == 1 or coefficient == 0:
            return ''
        if coefficient == -1:
            return '-'
        if 0 < coefficient < 1:
            return str(Fraction(coefficient))
        return str(coefficient)

    @staticmethod
    def str_powered_var(variable: str = 'x', degree: numbers = 1) -> str:
        """Convert a degree and variable to a of variable raised to degree.

        Args:
            `variable` (str, optional): The variable. Defaults to 'x'.
            `degree` (numbers, optional): The power/degree of variable.

        >>> Term.str_powered_var('x', 2)
        'x²'
        >>> Term.str_powered_var('x', 0)
        ''
        >>> Term.str_powered_var('x', 1)
        'x'
        >>> Term.str_powered_var('x', 0.5)
        'x^(1/2)'
        >>> Term.str_powered_var('y', 12)
        'y^12'
        """
        if degree == 0:
            return ''
        if degree == 1:
            return variable
        if 0 < degree < 1:
            return f'{variable}^({str(Fraction(degree))})'
        if 1 < degree <= 9:
            return f'{variable}{XDEGREE(degree).pwr}'
        return f'{variable}^{str(degree)}'

    @classmethod
    def fromstring(cls, term) -> object:
        """Create a Term from a term string.

        Args:
            term (str): A string term

        Returns:
            Term: A Term object form on the string term

        >>> Term.fromstring('1/4x³')
        Term(1/4, 'x', 3)
        """
        pattern = re.compile(r'([-+]?[(\d)/.d]*)([a-zA-Z]*)[\^]?(.*)')
        match = pattern.match(term)
        if match:
            coefficient, variable, power = match.groups()
            if coefficient == '-':
                coefficient = '-1'
            elif coefficient == '+' or coefficient == '':
                coefficient = '1'
            coefficient = convert_to_numeric(coefficient)
            power = XDEGREE.powers().get(power, power)
            if isinstance(power, str):
                if power == '':
                    if variable == '':
                        power = '0'
                    else:
                        power = '1'
                power = convert_to_numeric(power)
            if variable == '':
                variable = 'x'
            return Term(coefficient, variable, power)

    @property
    def parts(self) -> tuple:
        """The parts of the term in order: coefficient, variable, degree.

        >>> Term(5, 'x', 2).parts
        (5, 'x', 2)
        """
        return tuple(self._parts)

    @parts.setter
    def parts(self, in_parts) -> None:
        """
        Sets the term coefficient, variable, and degree.

        Args:
            coefficient (numbers): The term's coefficient.
            variable (str): The term's variable.
            degree (numbers): The degree of the term.

        >>> term = Term(5, 'x', 2)
        >>> term.parts = [6, 'x', 3]
        >>> term.parts
        (6, 'x', 3)
        """
        self.coeff, self.variable, self.degree = in_parts
        self._parts = [self.coeff, self.variable, self.degree]

    def __lt__(self, __o: object) -> bool:
        """Evaluate whether self is less than other.

        Raises:
            NotImplementedError: If __o is not a Term or if variables
                do not match between self and __o.

        Returns:
            bool: Returns True if self is less than __o.

        >>> term1 = Term(1, 'x', 2)
        >>> term2 = Term(4, 'x', 1)
        >>> term3 = Term(1, 'x', 2)
        >>> term1 < term2
        False
        >>> term1 > term2
        True
        >>> term1 < term3
        False
        """
        if not isinstance(__o, Term):
            raise NotImplementedError(f"{__o} Must be Term not {type(__o)}")
        if not self.variable == __o.variable and not (__o.degree == 0
                                                      or self.degree == 0
                                                      ):
            raise NotImplementedError('Cannot compare different variables')
        if self.degree < __o.degree:
            return True
        return False

    def __le__(self, __o: object) -> bool:
        """Evaluate whether self is less than or equal to other.

        Raises:
            NotImplementedError: If __o is not a Term or if variables
                do not match between self and __o.

        Returns:
            bool: Returns True if self is less than __o.

        >>> term1 = Term(1, 'x', 2)
        >>> term2 = Term(4, 'x', 1)
        >>> term3 = Term(1, 'x', 2)
        >>> term1 <= term2
        False
        >>> term1 >= term1
        True
        >>> term1 <= term3
        True
        """
        if not isinstance(__o, Term):
            raise NotImplementedError(f"{__o} Must be Term not {type(__o)}")
        if not self.variable == __o.variable and not (__o.degree == 0
                                                      or self.degree == 0
                                                      ):
            raise NotImplementedError('Cannot compare different variables')
        if self.degree <= __o.degree:
            return True
        return False

    def __eq__(self, __o: object) -> bool:
        """Evaluate whether self is equal to other.

        Raises:
            NotImplementedError: If __o is not a Term or if variables
                do not match between self and __o.

        Returns:
            bool: Returns True if self is less than __o.

        >>> term1 = Term(1, 'x', 2)
        >>> term2 = Term(4, 'x', 1)
        >>> term3 = Term(1, 'x', 2)
        >>> term1 == term2
        False
        >>> term2 == term1
        False
        >>> term1 == term3
        True
        """
        if not isinstance(__o, Term):
            raise NotImplementedError(f"{__o} Must be Term not {type(__o)}")
        if not self.variable == __o.variable and not (__o.degree == 0
                                                      or self.degree == 0
                                                      ):
            raise NotImplementedError('Cannot compare different variables')
        if self.degree == __o.degree:
            return True
        return False

    def __add__(self, __o: object) -> object:
        """Add other to self.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.

        >>> term1 = Term(1, 'x', 2)
        >>> term2 = Term(4, 'x', 2)
        >>> term1 + term2
        Term(5, 'x', 2)
        """
        if not isinstance(__o, Term):
            raise NotImplementedError(f"{__o} Must be Term not {type(__o)}")
        if not self.variable == __o.variable:
            raise NotImplementedError('Cannot compare different variables')
        if not self.degree == __o.degree:
            raise NotImplementedError('Cannot add terms of different degrees')
        return Term(self.coeff + __o.coeff, self.variable,
                    self.degree)

    def __sub__(self, __o: object) -> object:
        """Subtract other from self.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.

        >>> term1 = Term(1, 'x', 2)
        >>> term2 = Term(4, 'x', 2)
        >>> term1 - term2
        Term(-3, 'x', 2)
        """
        if not isinstance(__o, Term):
            raise NotImplementedError(f"{__o} Must be Term not {type(__o)}")
        if not self.variable == __o.variable:
            raise NotImplementedError('Cannot compare different variables')
        if not self.degree == __o.degree:
            raise NotImplementedError('Cannot add terms of different degrees')
        return Term(self.coeff - __o.coeff, self.variable,
                    self.degree)

    def __mul__(self, __o: object) -> object:
        """Multiply self and other.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.

        >>> term1 = Term(1, 'x', 2)
        >>> term2 = Term(4, 'x', 2)
        >>> term1 * term2
        Term(4, 'x', 4)
        """
        if not isinstance(__o, Term):
            raise NotImplementedError(f"{__o} Must be Term not {type(__o)}")
        if not self.variable == __o.variable and not (__o.degree == 0
                                                      or self.degree == 0
                                                      ):
            raise NotImplementedError('Cannot multiply different variables')
        return Term(self.coeff * __o.coeff, self.variable,
                    self.degree + __o.degree)

    def __truediv__(self, __o: object) -> bool:
        """Divide self by other.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.

        >>> term1 = Term(1, 'x', 2)
        >>> term2 = Term(4, 'x', 1)
        >>> term1 / term2
        Term(0.25, 'x', 1)
        """
        if not isinstance(__o, Term):
            raise NotImplementedError(f"{__o} Must be Term not {type(__o)}")
        if not self.variable == __o.variable and not (__o.degree == 0
                                                      or self.degree == 0
                                                      ):
            raise NotImplementedError('Cannot divide different variables')
        return Term(self.coeff / __o.coeff, self.variable,
                    self.degree - __o.degree)

    def __floordiv__(self, __o: object) -> bool:
        """Floor divide self by other.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.

        >>> term1 = Term(5, 'x', 2)
        >>> term2 = Term(2, 'x', 1)
        >>> term1 // term2
        Term(2, 'x', 1)
        """
        if not isinstance(__o, Term):
            raise NotImplementedError(f"{__o} Must be Term not {type(__o)}")
        if not self.variable == __o.variable and not (__o.degree == 0
                                                      or self.degree == 0
                                                      ):
            raise NotImplementedError('Cannot divide different variables')
        return Term(self.coeff // __o.coeff, self.variable,
                    self.degree - __o.degree)

    def __mod__(self, __o: object) -> bool:
        """Divide self by other.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.

        >>> term1 = Term(5, 'x', 2)
        >>> term2 = Term(2, 'x', 1)
        >>> term1 % term2
        Term(1, 'x', 1)
        """
        if not isinstance(__o, Term):
            raise NotImplementedError(f"{__o} Must be Term not {type(__o)}")
        if not self.variable == __o.variable and not (__o.degree == 0
                                                      or self.degree == 0
                                                      ):
            raise NotImplementedError('Cannot mod different variables')
        return Term(self.coeff % __o.coeff, self.variable,
                    self.degree - __o.degree)


# [ ] Create a polynomail function class that uses (or replaces) functions
class Polynomial:
    def __init__(self, terms: list[Term]) -> None:
        terms.sort(reverse=True)
        self.terms = terms
        self.coefficients = [t.coeff for t in terms]

    def __repr__(self) -> str:
        return f'Polynomial({self.terms})'

    def __str__(self) -> str:
        """
        Return the string version of the term.

        Returns:
            str: The string version of the term.

        >>> term = Polynomial([Term(1, 'x', 1), Term(3, '', 0)])
        >>> str(term)
        'x + 3'
        """
        polynomial = []
        for i, term in enumerate(self.terms):
            a = term.coeff
            if i != 0:
                if a > 0:
                    polynomial.append('+')
                    polynomial.append(str(term))
                elif a < 0:
                    polynomial.append('-')
                    polynomial.append(abs(a), term.variable, term.degree)
        return ' '.join(polynomial)

    def __container__(self) -> list:
        return self.coefficients

    def __len__(self) -> int:
        return len(self.coefficients)

    @staticmethod
    def makestring(coefficients: list) -> str:
        """Returns a string polynomial

        Args:
            coefficients (list): The coefficients ordered from degree
             descending.

        Returns:
            str: The string polynomial

        >>> Polynomial.makepolynomial([-1, 0.25, 12, -2, 3])
        '-x⁴ + 1/4x³ + 12x² - 2x + 3'
        """
        polynomial = []
        degree = len(coefficients) - 1
        # Create the polynomial
        for i, a in enumerate(coefficients):
            # If a is negative, add a minus sign between terms.
            if i != 0:
                if a > 0:
                    polynomial.append('+')
                elif a < 0:
                    polynomial.append('-')
                    a = abs(a)
                else:
                    degree -= 1
                    continue

            # Add the terms with x to the appropriate power.
            if degree >= 0:
                polynomial.append(str(Term(a, 'x', degree)))
            else:
                break
            degree -= 1
        return ' '.join(polynomial)

    @classmethod
    def fromcoefficients(cls, coefficients: list[int] = None,
                         variable='x') -> object:
        """Prompt user to provide coefficients for a polynomial.
        """
        terms = []
        # Create polynomial given coefficients passed to method.
        if coefficients:
            if [a for a in coefficients
                    if not isinstance(a, (int, float, Fraction))]:
                # Raise error of coefficients are not all integers.
                raise TypeError('Coefficients must be integers.')
            degree = len(coefficients) - 1
            for i, a in enumerate(coefficients):
                if degree < 0:
                    break
                terms.append(Term(a, variable, degree))
                degree -= 1

            return Polynomial(terms)

        # If no coefficient passed to function, obtain from terminal input.
        # Get polynomial's degree for number of coefficients to request
        polynomialdegree = int(input('Enter the degree of the polynomial: '))

        if polynomialdegree < 0:
            raise ValueError('The degree of the polynomial cannot be negative')

        # Ask user to provide coefficients by power of x to ensure all
        # provided and provided in order.
        for i in range(polynomialdegree, -1, -1):
            while True:
                coefficient = input(f'Enter coefficient for x^{i}: ').strip()
                # Need to remove '-' for isnumeric() used later.
                if coefficient.startswith('-'):
                    coefficient = coefficient.replace('-', '')
                    sign = -1
                elif coefficient.startswith('+'):
                    coefficient = coefficient.replace('+', '')
                    sign = 1
                else:
                    sign = 1
                # Convert string coefficient to int, Fraction, or Complex
                if coefficient.isnumeric():
                    terms.append(Term(coefficient * sign, 'x', i))
                    break
                else:
                    print('Coefficients must be integers.')
        return Polynomial(terms)

    @classmethod
    def fromstring(cls, polynomial: str) -> object:
        """Create a Polynomial object from a string polynomial.

        Args:
            polynomial (str): The string polynomial.

        Returns:
            Polynomial: A Polynomial object.

        >>> Polynomial.fromstring('-x⁴ + 1/4x³ - 3')
        Polynomial([Term(-1, 'x', 4), Term(1/4, 'x', 3), Term(-3)])
        """
        sign = ''
        terms = []
        for t in polynomial.split(' '):
            if t == '+':
                sign = ''
                continue
            if t == '-':
                sign = '-'
                continue
            terms.append(Term.fromstring(f'{sign}{t}'))
        terms.sort()
        return Polynomial(terms)

    @property
    def possible_zeros(self) -> list:
        """Rational Zeros Theorem possible zeros of a polynomial function.

        Returns:
            list: A list containing all possible zeros, negative and positive.
        """
        zeros = []
        # Obtain factors of a_n and a_0
        factors_an = get_factors(self.coefficients[0])
        factors_a0 = get_factors(self.coefficients[-1])
        # Generate all possible zeros, skipping duplicates.
        for i in factors_a0:
            zeros.extend([i, -i])
            for j in factors_an:
                frac = Fraction(i, j)
                if frac not in zeros:
                    zeros.extend([frac, -frac])
        # Sort the possible zeros in absolute value order.
        zeros.sort(key=abs)
        return zeros

    def divide_by_x_minus(self, c: Fraction | int) -> tuple[list]:
        """Obtain the quotient result of dividing a polynomial by x - {x_minus}

        Returns:
            (tuple): The quotient's coefficients, and the remainder.
        """
        last_coefficient_index = len(self.coefficients) - 1
        remainder = 0
        quotient_coefficients = []
        # Obtain the remainder and quotient using synthetic division.
        for i, a in enumerate(self.coefficients):
            # Obtain quotient, convert int floats and Fractions to int.
            underline = (remainder + a)
            if isinstance(underline, (float, Fraction)):
                underline = convert_to_int(underline)
            if i != last_coefficient_index:
                quotient_coefficients.append(underline)
                # Calculate remainder
                remainder = (underline) * c
            else:
                remainder = underline
        # Convert int floats and Fractions to int.
        if isinstance(remainder, (float, Fraction)):
            remainder = convert_to_int(remainder)
        return quotient_coefficients, remainder

    @property
    def realzeros(self) -> dict:
        """Return zero(s) of a polynomial function with coefficients."""
        # Obtain all possible zeros using the rational zeros theorem.
        possiblezeros = self.possible_zeros
        # Test all possible zeros, saving any whose remainder is zero.
        return [possiblezero for possiblezero in possiblezeros
                if self.divide_by_x_minus(possiblezero)[1] == 0]

    def __lt__(self, __o: object) -> bool:
        """Evaluate whether self is less than other.

        Raises:
            NotImplementedError: If __o is not a Term or if variables
                do not match between self and __o.

        Returns:
            bool: Returns True if self is less than __o.
        """
        if not isinstance(__o, Polynomial):
            raise NotImplementedError(
                f"{__o} Must be Polynomial not {type(__o)}")
        return self.terms[0] < __o.terms[0]

    def __le__(self, __o: object) -> bool:
        """Evaluate whether self is less than or equal to other.

        Raises:
            NotImplementedError: If __o is not a Term or if variables
                do not match between self and __o.

        Returns:
            bool: Returns True if self is less than __o.
        """
        if not isinstance(__o, Polynomial):
            raise NotImplementedError(
                f"{__o} Must be Polynomial not {type(__o)}")
        return self.terms[0] <= __o.terms[0]

    def __eq__(self, __o: object) -> bool:
        """Evaluate whether self is equal to other.

        Raises:
            NotImplementedError: If __o is not a Term or if variables
                do not match between self and __o.

        Returns:
            bool: Returns True if self is less than __o.
        """
        if not isinstance(__o, Polynomial):
            raise NotImplementedError(
                f"{__o} Must be Polynomial not {type(__o)}")
        return self.terms[0] == __o.terms[0]

    def __add__(self, __o: object) -> object:
        """Add other to self.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.
        """
        if not isinstance(__o, Polynomial):
            raise NotImplementedError(
                f"{__o} Must be Polynomial not {type(__o)}")
        return Polynomial(
            [p1 + p2 for p1, p2 in zip(self.terms, __o.terms)])

    def __sub__(self, __o: object) -> object:
        """Subtract other from self.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.
        """
        if not isinstance(__o, Polynomial):
            raise NotImplementedError(
                f"{__o} Must be Polynomial not {type(__o)}")
        return Polynomial(
            [p1 - p2 for p1, p2 in zip(self.terms, __o.terms)])

    def __mul__(self, __o: object) -> object:
        """Multiply self and other.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.
        """
        if not isinstance(__o, Polynomial):
            raise NotImplementedError(
                f"{__o} Must be Polynomial not {type(__o)}")
        return Polynomial(
            [p1 * p2 for p1, p2 in zip(self.terms, __o.terms)])

    def __truediv__(self, __o: object) -> bool:
        """Divide self by other.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.
        """
        if not isinstance(__o, Polynomial):
            raise NotImplementedError(
                f"{__o} Must be Polynomial not {type(__o)}")
        return Polynomial(
            [p1 / p2 for p1, p2 in zip(self.terms, __o.terms)])

    def __floordiv__(self, __o: object) -> bool:
        """Floor divide self by other.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.
        """
        if not isinstance(__o, Polynomial):
            raise NotImplementedError(
                f"{__o} Must be Polynomial not {type(__o)}")
        return Polynomial(
            [p1 // p2 for p1, p2 in zip(self.terms, __o.terms)])

    def __mod__(self, __o: object) -> bool:
        """Divide self by other.

        Raises:
            NotImplementedError: If __o is not a Term, and if either
                the degree or variable of self and other do not match.
        """
        if not isinstance(__o, Polynomial):
            raise NotImplementedError(
                f"{__o} Must be Polynomial not {type(__o)}")
        return Polynomial(
            [p1 % p2 for p1, p2 in zip(self.terms, __o.terms)])


def print_factoring(poly: Polynomial) -> None:
    factors = []
    # Factor out the real zeros, printing the results
    factoring_coeff = poly.coefficients
    # Obtain real zeros
    zeros = poly.realzeros
    if zeros:
        print(f'\nThe real {"zeros" if len(zeros) > 1 else "zero"}'
              f' for {str(poly)}',
              f'\n{"are" if len(zeros) > 1 else "is"}:'
              f'  {", ".join(map(str, zeros))}')
        print('\nFactoring...')
    else:
        print('No real zeros found.')

    # Factor out real zeros using synthetic division
    for real_zero in zeros:
        quotient, remainder = poly.divide_by_x_minus(real_zero)
        factors.append(Polynomial.fromcoefficients([1, real_zero * -1]))
        parts = [Polynomial.fromcoefficients(factoring_coeff),
                 Polynomial.fromcoefficients(quotient)]
        print()
        if parts[0] == poly:
            field_width = max(map(len, parts)) + 1
        print(f'\t{str(parts[0]):>{field_width + 3}}',
              f'\t {chr(247)} {str(factors[-1]):>{field_width}}',
              f'\t{"=" * (field_width+3):>{field_width+3}}',
              f'\t{str(parts[1]):>{field_width + 3}}',
              sep='\n', end='\t')
        print(f'  {remainder = !s}')
        factoring_coeff = quotient
    print()

    # See if possible to get non-real zeros.
    if len(quotient) == 3:
        quadratic_formula_parts = quadratic_formula(quotient)
        print(f'\nThe non-real zeros for {poly}',
              '\nare:', end=" ")
        print(f'{quadratic_formula_parts[0]} ± {quadratic_formula_parts[1]}')
        factors.extend([
            f'x - ({quadratic_formula_parts[0]} + {quadratic_formula_parts[1]}'
            ')',
            f'x - ({quadratic_formula_parts[0]} - {quadratic_formula_parts[1]}'
            ')'])
        print()

    print('Final factored form:')
    print(f'\t({")(".join([str(factor) for factor in factors])})')


def print_coefficients(poly: Polynomial, c) -> None:
    quotient, remainder = poly.divide_by_x_minus(c)
    parts = [str(poly), Polynomial.makestring([1, c * -1]),
             Polynomial.makestring(quotient)]
    field_width = max(map(len, parts)) + 1
    print(f'{parts[0]:>{field_width + 3}}',
          f' {chr(247)} {parts[1]:>{field_width}}',
          '=' * (field_width + 3),
          f'{parts[2]:>{field_width + 3}}',
          sep='\n', end='\t')
    print(f'  {remainder = !s}')


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    poly = Polynomial.fromcoefficients([2, -9, -35])
    print_factoring(poly)
    # print(poly.divide_by_x_minus(6))
