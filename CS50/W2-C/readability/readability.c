
#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int *count_contents(string text, int counts[]);

// Coleman-Liau index = 0.0588 * L * S - 15.8
// = round(0.0588 * (avgNumLetters/100words) * (avgNumSentences/100words) - 15.8)
int main(void)
{
    /*Declare array that will be passed to count_contents().
        counts[1] = 1 in order to count final word in text since what is actually counted is the number of spaces.*/
    int counts[] = {0, 1, 0};

    // Prompt user for the text to be evaluated.
    string text = get_string("Text: ");

    // Get the counts of letters, words, and sentences in the text.
    int *counted = count_contents(text, counts);
    int num_letters = counted[0];
    int num_words = counted[1];
    int num_sentences = counted[2];

    // Calculate Coleman-Liau Index: 0.0588 * L * S - 15.8
    float L = (num_letters / (float)num_words) * 100; // Average number of letters per 100 words.
    float S = (num_sentences / (float)num_words) * 100; // Average number of sentences per 100 words.
    int coleman_liau_index = round(0.0588 * L - 0.296 * S - 15.8);

    // Print the results.
    if (coleman_liau_index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (coleman_liau_index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", coleman_liau_index);
    }
}
int *count_contents(string text, int counts[])
{
    /* Count the number of letters, words, and sentences in the text.

    Returns a pointer to the beginning of the array to avoid unnecessary repetition.
    Source of how to do this:
        - Trial and error, and
        - https://docs.microsoft.com/en-us/cpp/c-language/return-type?view=msvc-170
    */
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // A letter is any lowercase character from a-z and A-Z.
        char letter = toupper(text[i]);  // Control for case.
        if (letter >= 65 && letter <= 90)
        {
            counts[0] += 1;
        }
        else if (text[i] == 32)
        {
            // A word is any sequence of characters with a space between.
            counts[1] += 1;
        }
        else if (text[i] == 33 || text[i] == 46 || text[i] == 63)
        {
            // A sentence ends in a period, exclamation mark, or question mark.
            counts[2] += 1;
        }
    }
    return counts;
}
