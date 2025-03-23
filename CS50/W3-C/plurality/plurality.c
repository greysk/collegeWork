#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // Search for candidates in candidates and increase votes if found.
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes += 1;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // If only one candidate, the single candidate is the winner.
    if (candidate_count == 0)
    {
        printf("%s", candidates[0].name);
        return;
    }
    // Sort candidates by vote (largest to smallest) to determine winner
    int num_sorted = 0;
    int most_index = 0;
    candidate most;
    do
    {
        for (int i = num_sorted; i < candidate_count; i++)
        {
            most = candidates[i];
            for (int j = num_sorted; j < candidate_count; j++)
            {
                if (candidates[j].votes >= most.votes)
                {
                    most = candidates[j];
                    most_index = j;
                }
            }
            candidates[most_index] = candidates[i];
            candidates[i] = most;
            num_sorted++;
        }
    }
    while (num_sorted < candidate_count);

    // Print out results including candidates tied for highest score.
    int i = 0;
    do
    {
        printf("%s\n", candidates[i].name);
        i++;
    }
    while (candidates[0].votes == candidates[i].votes);
    return;
}
