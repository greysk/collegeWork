#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

// Number of pairs and number of candidates in above arrays
int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    // Reset number of pairs
    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // Make sure vote is for a potential candidate before updating ranks.
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            // Record candidate's index in candidates[].
            ranks[rank] = i;
            return true;
        }
    }
    // Not acceptable candidate.
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // Add winning pairs from one voter's ranks to preferences.
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]] ++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            // Compare candidates[i] against candidates[j] and add pairs for winner
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count ++;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count ++;
            }
            // Do nothing if tied.
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int num_sorted = 0;
    int victory_strength = 0;
    int index4_more_preferred = 0;
    do
    {
        for (int i = num_sorted; i < pair_count; i++)
        {
            // Initially, assume that pairs[i]'s winner has strongest victory.
            pair more_preferred = pairs[i];
            index4_more_preferred = i;

            for (int j = num_sorted + 1; j < pair_count; j++)
            {
                // Obtain current more_preferred pair's victory strength.
                victory_strength = preferences[more_preferred.winner][more_preferred.loser];

                // Set new more_preferred pair a higher victory strength is found.
                if (preferences[pairs[j].winner][pairs[j].loser] > victory_strength)
                {
                    more_preferred = pairs[j];
                    index4_more_preferred = j;
                }
            }
            // Place pairs in decreasing order by strength of victory.
            if (index4_more_preferred != i)
            {
                pairs[index4_more_preferred] = pairs[i];
                pairs[i] = more_preferred;
            }
            num_sorted ++;
        }
    }
    while (num_sorted < pair_count);
    // All sorted.
    return;
}

// Tests if locking a pair would create a cycle.
bool is_cycle(int start_winner, int p_loser)
{
    bool cycles = false;
    int losers = 0;
    int losers_to_p_loser[pair_count];
    for (int j = 0; j < candidate_count; j++)
    {
        // Check if start_winner's loser is a winner in locked.
        if (locked[p_loser][j])
        {
            // Cycle found. Pointers lead back to start_winner.
            if (j == start_winner)
            {
                return true;
            }
            losers_to_p_loser[losers] = j;
            losers++;
        }
    }
    // Follow existing pointers to check if they lead back to start_winner.
    if (losers > 0)
    {
        for (int i = 0; i < losers; i++)
        {
            cycles = is_cycle(start_winner, losers_to_p_loser[i]);
        }
    }
    return cycles;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        pair p = pairs[i];
        // Check if locking pair would create a cycle.
        if (!(is_cycle(p.winner, p.loser)))
        {
            // No cycle would be created, lock pair into candidate graph.
            locked[p.winner][p.loser] = true;
        }
        // Skip pair since cycle would be created.
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        bool is_source = true;
        // Check if candidate is the source.
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                is_source = false;
                break;
            }
        }
        if (is_source)
        {
            // Candidate is the source, print result.
            printf("%s\n", candidates[i]);
            return;
        }
    }
    return;
}
