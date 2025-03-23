# Simulate a sports tournament
# Student's comment about topics not covered in class that may
# appear below: Python's my hobby language and I wrote this code
# using knowledge I have from that.

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # Read teams into memory from file
    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        for row in reader:
            teams.append({'team': row['team'], 'rating': int(row['rating'])})

    counts = {}
    # Simulate N tournaments and keep track of win counts
    for i in range(N):
        winner = simulate_tournament(teams)
        # If not already in counts, add winning team with a default
        # number of wins of 0.
        counts.setdefault(winner, 0)
        # Increase winning team's score by 1.
        counts[winner] += 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    round_teams = teams.copy()
    # Set round_teams to round winner until one team remains.
    while len(round_teams) > 1:
        round_teams = simulate_round(round_teams)
    return round_teams[0]['team']


if __name__ == "__main__":
    main()
