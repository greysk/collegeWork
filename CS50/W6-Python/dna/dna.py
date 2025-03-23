import csv
import sys
import re


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        # Incorrect number provided.
        print('Usage: python.exe <STR_counts>.csv <filename>.txt')
        return None

    database = sys.argv[1]
    sequence = sys.argv[2]

    # Read database file into a variable
    with open(database, 'r') as f:
        csv_data = [row for row in csv.reader(f)]

    # Read DNA sequence file into a variable
    with open(sequence, 'r') as f:
        dna = f.read()

    # Obtain a list of the STRs in the CSV file.
    STRs = csv_data[0][1:]

    # Find longest match of each STR in DNA sequence
    dna_str_counts = [longest_match(dna, Str) for Str in STRs]

    # For each row, map the STR columns to the name column.
    suspects = {row[0]: [int(cell) for cell in row[1:]]
                for row in csv_data[1:]}

    # Check database for matching profiles
    for suspect, suspect_str_counts in suspects.items():
        # For each STR, compare the STR count of the suspect to the DNA.
        dna_match = [suspect_str_counts[i] == dna_str_counts[i]
                     for i in range(len(STRs))]
        # Check if all of the STR counts for suspect and DNA were the same.
        if all(dna_match):
            # Match found.
            print(suspect)
            return None
    # No suspect matched the DNA.
    print('No match')
    return None


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
