# Tennis-Ranking-System
Implementation of tennis ranking system for DADSA coursework part A

THE ASSIGNMENT BRIEF:

A New Professional Association of Tennis Players has started a New Tennis Tournament
Circuit.The first season will start with just four tournaments which will take place at different times
of the year in different locations.

Each tournament has been assigned a degree of difficulty.

- Each tournament has prize money awarded to every player that reaches the last eight.
- Each tournament has two competitions for Men and Women singles
- Each place in the top sixteen is awarded a given number of ranking points

You are required to design, implement and evaluate a simple system that takes as input the
score for each match for a given tournament and updates each player’s position, calculates
each player’s ranking points and produces a list of the players ranking in descending order.
The system calculates the prize money due to each player at any given point in time and
accumulates these having stored them safely.

The four tournaments are listed below:
- TAC1 – degree of difficulty 2.7
- TAE21 – degree of difficulty 2.3
- TAW11 – degree of difficulty 3.1
- TBS2 – degree of difficulty 3.25

The first season has attracted 32 men and 32 women players in total and details of these
players are given to you in separate files. The prize money awarded for each of the eight top positions for each tournament is also
given to you in a file.

- Your system should check for erroneous double entries of results.
- The system should also check for the validity of scores entered – i.e. one player in the men’s
game must have three sets per match, but no two players can have three sets in the same
match. Similarly, in the ladies game the winner in a match must win two sets and no two
players can win two sets each in the same match.
- Match results should show the score in terms of sets won for each player. A win in the men
circuit is on best of five and a win in the women circuit is on best of three.

Assumptions:
- In calculating the rating points the standard tournament place points will be multiplied
by the degree of difficulty.
- Each match’s score must be represented as Player A, number of sets A, Player B,
number of sets B.
- The winner is the player that has won three set in the men’s game or two sets in the
ladies game.
- Scores should be read either from a file or entered manually from the prompt. A
simple User Interface with a menu selection should be offered.
