import re

from cs50 import get_string


def test_credit(number: str) -> None:
    """
    Test a credit card number and, if valid, prints the bank name.

    Prints INVALID if number is not validated as a credit card number.

    Args:
        number (str | int): The credit card number to test.
    """
    # Define dictionary containing tests for credit card name.
    basic_test = {'4': ({13, 16}, 'VISA'),
                  '5': ({16}, 'MASTERCARD'),
                  '3': ({15}, 'AMEX')}

    # Test to ensure the first digit(s) in the card are valid.  Based on the
    # following rules: Visa numbers start with 4; American Express numbers
    # start with 34 or 37; and MasterCard numbers start with 51, 52, 53, 54, or 55.
    pattern = re.compile(r'^(4.|3[47]|5[1-5])')
    match = pattern.match(number)
    if not match:
        print('INVALID')
        return None

    # Test if the number of digits align to first digit of the card number.
    # Based on the following rules: American Express uses 15-digit numbers;
    # MasterCard uses 16-digit numbers; and Visa uses 13- and 16-digit numbers
    num_digits = len(number)
    first_digit = match.group(1)[0]
    if num_digits not in basic_test[first_digit][0]:
        print('INVALID')
        return None

    # Perform steps 1 and 2 of Luhn’s Algorithm: (1) Starting from 2nd-to-last
    # digit, multiply every other digit by 2 and sum the digits of the results;
    # (2) Add step 1's sum to the sum of the remaining digits from the number
    # (the sum of every other digit from the last digit of the number).
    algorithm = (sum([int(i) * 2 // 10 + (int(i) * 2 % 10)
                      for i in number[-2::-2]])
                 + sum([int(i) for i in number[-1::-2]])
                 )

    # Perform step 3 of Luhn's Algorithm: Check if the sum from step 1 and 2 end with 0.
    if algorithm % 10 != 0:
        print('INVALID')
        return None

    # All tests passed. Print the name of the Financial Intitution for the card.
    print(basic_test[first_digit][1])


if __name__ == '__main__':
    card_number = get_string('Number: ')
    test_credit(card_number)
