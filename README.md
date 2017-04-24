# Tournament Database

This was a project for Udacity's Full-Stack Nanodegree sequence, course Introduction to Relational Databases.

It uses PostgresSQL and Python to create and query a database containing outcomes for a Swiss-system tournament. 

To run the application, please log into your virtual machine and place the application files in your synced folders.

Then:

```

# Enter the psql CLI
psql

# Create database
psql$ CREATE DATABASE tournament;

# Connect to the newly created tournament database
psql$ \c tournament;

# Create tables and views
psql$ \i tournament.sql;

# Exit out of the psql CLI
\q

# Run Python test files
python tournament_test.py 

```
