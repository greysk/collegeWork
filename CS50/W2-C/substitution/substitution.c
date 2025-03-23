#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string encrypt_text(string key, string text);
string check_key(string key);

int main(int argc, string argv[])
{
    string cipher_key;
    // Check for proper amount of command line arguments.
    if (argc != 2)
    {
        // Improper amount of command line arguments provided.
        printf("Usage: ./substitution key\n");
        return 1;
    }
    // Ensure cypher key provided is the correct length.
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    // Check cipher_key contents for any non-alphabetic characters or repeated letters.
    else
    {
        cipher_key = check_key(argv[1]);
    }

    // Check if check_key() returned failure code instead of cypher key.
    if (cipher_key[0] == '0')
    {
        printf("Key must contain only alphabetic characters and each letter can only be used once.\n");
        return 1;
    }
    // All tests passed.

    // Prompt for text to be encrypted.
    string plaintext = get_string("plaintext: ");

    // Encrypt text.
    string encrypted = encrypt_text(cipher_key, plaintext);


    printf("ciphertext: %s", encrypted);
    printf("\n");
    return 0;
}
string check_key(string key)
{
    // Ensure cypher key is acceptable.
    for (int i = 0; key[i] != '\0'; i++)
    {
        // Check for non alphabetic characters in cypher key.
        if (key[i] < 65 || (key[i] > 90 && key[i] < 97) || key[i] > 122)
        {
            return "0";

        }
        // Check for any duplicate letters in cypher key.
        for (int j = 0; key[j] != '\0'; j++)
        {
            if (key[i] == key[j] && i != j)
            {
                return "0";
            }
        }
    }
    return key;
}
string encrypt_text(string key, string text)
{
    // Replace letters in text with cipher key letter.
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // Make capital letters zero-indexed where A = 0.
        int index_in_key = text[i] - 65;
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            // Input letter is lowercase, take 32 off to get to index 0.
            index_in_key -= 32;
            text[i] = tolower(key[index_in_key]);
        }
        else if (text[i] >= 'A' && text[i] <= 'Z')
        {
            // Input letter is uppercase.
            text[i] = toupper(key[index_in_key]);
        }
        // Input character is not a letter, don't change anything.
        text[i] = text[i];
    }
    return text;
}
