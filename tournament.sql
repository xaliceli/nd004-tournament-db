-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drops tables and views if they already exist to prevent duplication errors.
-- Starting with views first and working backwards so that all dependencies
-- are deleted before deleting table.

DROP VIEW IF EXISTS player_matches;
DROP VIEW IF EXISTS player_wins;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

-- Create table to store player data.

CREATE TABLE players (
	player_id serial PRIMARY KEY,
	player_name text
);

-- Create table to store match data.

CREATE TABLE matches (
	match_id serial PRIMARY KEY,
	player_1 integer REFERENCES players (player_id),
	player_2 integer REFERENCES players (player_id),
	winner integer REFERENCES players (player_id)
);

-- Create view to summarize the number of wins by player.

CREATE VIEW player_wins AS 
	SELECT players.player_id, players.player_name, 
		   count(matches.winner) as wins
	FROM players LEFT JOIN matches 
		ON players.player_id = matches.winner 
	GROUP BY players.player_id;

-- Create view to summarize the number of matches by player.

CREATE VIEW player_matches AS
	SELECT players.player_id, players.player_name, 
		   count(matches.match_id) as matches
	FROM players LEFT JOIN matches 
		ON players.player_id = matches.player_1 
		OR players.player_id = matches.player_2
	GROUP BY players.player_id;