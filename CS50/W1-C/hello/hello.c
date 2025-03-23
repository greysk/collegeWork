#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Obtain user's name.
    string name = get_string("What's your name? ");
    // Greet user by name.
    printf("Hello, %s\n", name);
}
