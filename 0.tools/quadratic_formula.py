from fractions import Fraction
from math import sqrt


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
    print(sqrt(abs(determinate)))

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


if __name__ == '__main__':
    quadratic_formula()
