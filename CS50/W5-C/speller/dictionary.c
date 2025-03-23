// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 60000;

// Hash table
node *table[N];

// Function to free and count linked lists in table.
void count_linked(node *linked);
void free_linked(node *linked);

int dict_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to determine hash table index.
    int hashed = hash(word);
    // Check word hash table index and any linked lists thereat.
    node *to_check = table[hashed];
    while (to_check != NULL)
    {
        if (strcasecmp(word, to_check->word) == 0)
        {
            // Match found, word is spelled correctly.
            return true;
        }
        // Check next linked note at hash index.
        to_check = to_check->next;
    }
    // Word not found in dictionary.
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    // Use first 30 letters (or length on string - 1) to create hash value.
    for (int i = 0; i < 30 && i < strlen(word) - 1; i++)
    {
        /* Index letters alphabetically with a == 0 plus i
          so a, aa, and aaa do not all equal 0. */
        hash += ((word[i]) % 32 + i);
        if (i > 0)
        {
            hash += 25 * hash;
        }
    }
    // Obtain modulus of N incase hash is larger than table array.
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        // Unable to open file.
        return false;
    }
    char tmp[LENGTH + 1];
    // Read each word from dictionary into tmp until end of dictionary reached.
    while (fscanf(dict, "%s", tmp) >= 0)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            free(new_node);
            return false;
        }
        // Initialize new_node and copy word from dictionary into new_node.
        strcpy(new_node->word, tmp);
        new_node->next = NULL;
        // Place dictionary word into hash table.
        int hashed = hash(new_node->word);
        if (table[hashed] == NULL)
        {
            table[hashed] =  new_node;
        }
        else
        {
            new_node->next = table[hashed];
            table[hashed] = new_node;
        }
    }
    // All words copied into memory.
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Traverse hash table
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            // Count node at hash table and any linked lists.
            count_linked(table[i]);
        }
    }
    return dict_size;
}

// Count every linked list at hash table index.
void count_linked(node *linked)
{
    if (linked->next == NULL)
    {
        // Last node in linked list. Count it and return.
        dict_size += 1;
        return;
    }
    else
    {
        // Count back from end of linked list to hash table index.
        count_linked(linked->next);
        dict_size += 1;
    }
    return;
}


// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            // Free any nodes in linked list as hash table location
            free_linked(table[i]);
            // All linked list nodes freed. Remove pointer from array.
            table[i] = NULL;
        }
        if (table[i] != NULL)
        {
            // Unloading hash index failed.
            return false;
        }
    }
    // All memory freed.
    return true;
}

// Free linked list nodes working backwards from last node.
void free_linked(node *linked)
{
    if (linked->next == NULL)
    {
        // Last node in linked list. Free it and return.
        free(linked);
        return;
    }
    else
    {
        free_linked(linked->next);
        // Node pointed to by linked->next freed. Remove pointer to it.
        linked->next = NULL;
        // Free current node.
        free(linked);
    }
    // All linked lists nodes freed.
    return;
}
