#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    c = connection.cursor()
    c.execute("DELETE FROM matches")
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    c = connection.cursor()
    c.execute("DELETE FROM players")
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    c = connection.cursor()
    c.execute("SELECT COUNT(*) from players")
    count = c.fetchall()
    return count[0][0]
    connection.commit()
    connection.close()


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    c = connection.cursor()
    c.execute("INSERT INTO players VALUES (DEFAULT, %s)",
              (bleach.clean(name),))
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    c = connection.cursor()
    c.execute("""SELECT player_wins.player_id, player_wins.player_name,
                        player_wins.wins, player_matches.matches
                 FROM player_wins JOIN player_matches
                 ON player_wins.player_id = player_matches.player_id
                 ORDER BY player_wins.wins DESC""")
    standings = c.fetchall()
    return standings
    connection.commit()
    connection.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    c = connection.cursor()
    c.execute("INSERT INTO matches VALUES (DEFAULT, %s, %s, %s)",
              (winner, loser, winner,))
    connection.commit()
    connection.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    connection = connect()
    c = connection.cursor()
    c.execute("""SELECT player_wins.player_id, player_wins.player_name,
                        player_wins.wins, player_matches.matches
                 FROM player_wins JOIN player_matches
                 ON player_wins.player_id = player_matches.player_id
                 ORDER BY player_wins.wins DESC""")
    standings = c.fetchall()
    connection.commit()
    connection.close()

    pairings = []
    i = 0

    while i < len(standings):
        pairings.append((standings[i][0],
                         standings[i][1],
                         standings[i + 1][0],
                         standings[i + 1][1]))
        i += 2

    return pairings
