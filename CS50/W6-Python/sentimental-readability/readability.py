""" Calculate the readability of a given text using the Coleman-Liau index.

Coleman-Liau Index is 0.0588 * L - 0296 * S - 15.8
    L = average number of letters per 100 words.
    S = the average number of sentences per 100 words.
"""
import re

from cs50 import get_string

# Obtain text from user.
text = get_string('Text: ')

# Calculate the number of words, sentences, and letters in the text.
num_words = len(text.split(' '))
num_sentences = len(re.findall(r'[.?!]', text))
num_letters = len(re.findall(r'[a-zA-Z]', text))

# Calculate L and S for the Coleman-Liau Index.
L = num_letters / num_words * 100
S = num_sentences / num_words * 100

# Calculate the Coleman-Liau Index.
coleman_liau_index = round(0.0588 * L - 0.296 * S - 15.8)

# Determine the grade level of the text.
if coleman_liau_index < 1:
    print('Before Grade 1')
elif coleman_liau_index > 16:
    print('Grade 16+')
else:
    print(f'Grade {coleman_liau_index}')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
