#include <stdio.h>
#include <cs50.h>

// Functions used and defined below.
int get_num_digits(long number);
int get_first2digits(long number, int num_digits);
string card_bank(int first2digits, int num_digits);

int main(void)
{
    // Prompt user for credit card number.
    long card_number = get_long("Number: ");

    int second_last_x2 = 0;
    int step1_sum = 0;

    int step2_sum = 0;

    // Obtain the number of digits in the card number.
    int num_digits = get_num_digits(card_number);

    // Obtain the first two digits of the card number.
    int first2digits = get_first2digits(card_number, num_digits);

    /* Perform step 1 & step 2 of Luhn's Algorithm on every 2 digits in the
    card number starting from the right-most digits. */
    do
    {
        // Step 2, Part 1: From the last digit, add every other digit together.
        step2_sum += card_number % 10;

        // Remove last digit from card number since we're done with it.
        card_number /= 10;

        /* Step 1: From the 2nd to last digit, multiply every other digit by 2 and add the digit(s) of the result together. */
        second_last_x2 = (card_number % 10) * 2;
        if (second_last_x2 > 9)
        {
            step1_sum = (second_last_x2 / 10) + (second_last_x2 % 10);
        }
        else
        {
            step1_sum = second_last_x2;
        }

        // Step 2, Part 2: Add result of step 1 to step2_sum.
        step2_sum += step1_sum;

        // Remove 2nd last digit from card number since we're done with it.
        card_number /= 10;
    }
    while (card_number > 0);

    // Step 3 of Luhn's Algorithm: Check if last digit of step2_sum is 0.
    if (step2_sum % 10 == 0)
    {
        printf("%s", card_bank(first2digits, num_digits));
    }
    else
    {
        printf("INVALID\n");
    }
}
int get_num_digits(long number)
// Returns the number of digits contained in number.
{
    int i = 0;
    do
    {
        i += 1;
        number /= 10;
    }
    while (number > 0);
    return i;
}
int get_first2digits(long number, int num_digits)
// Returns the first two digits of number.
{
    for (int i = 0; i < num_digits - 2; i++)
    {
        number /= 10;
    }
    return number;
}
string card_bank(int first2digits, int num_digits)
/* Returns the bank for the credit card number or INVALID determined by using the first two digits and the number of digits in the card number. */
{
    if (num_digits == 15 && (first2digits == 34 || first2digits == 37))
    {
        return "AMEX\n";
    }
    if (num_digits == 16 && (first2digits >= 51 && first2digits <= 55))
    {
        return "MASTERCARD\n";
    }
    if ((num_digits == 13 || num_digits == 16) && first2digits / 10 == 4)
    {
        return "VISA\n";
    }
    return "INVALID\n";
}
