#include <stdio.h>
#include <cs50.h>

// Prints half a row for the pyramid. Used and defined below.
void make_partial_row(int num_hashmarks);

int main(void)
{
    // Prompt user for pyramid height
    int height = 0;
    do
    {
        height = get_int("Pyramid height: ");
    }
    while (height < 1 || height > 8);

    // Generate pyramid
    for (int i = 0; i < height; i++) // 0, 1
    {
        for (int j = i + 1; j < height; j++)
        {
            printf(" ");
        }
        make_partial_row(i + 1);
        printf("  ");
        make_partial_row(i + 1);
        printf("\n");
    }
}
void make_partial_row(int num_hashmarks)
/* Print the hascdhmarks part of a pyramid given the number of hashmarks to print.*/
{
    for (int k = 0; k < num_hashmarks; k++)
    {
        printf("#");
    }
}
