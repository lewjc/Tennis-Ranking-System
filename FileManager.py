import csv
import os
from ADT import *
from TournamentClasses import *
import re


def get_main_data():
    # defined data directory
    data_directory = os.path.dirname(__file__)

    file_name = "Data/MALE PLAYERS.csv"
    full_path = os.path.join(data_directory, file_name)
    male_players = import_players(open_file(full_path))

    file_name = "Data/FEMALE PLAYERS.csv"
    full_path = os.path.join(data_directory, file_name)
    female_players = import_players(open_file(full_path))

    file_name = "Data/RANKING POINTS.csv"
    full_path = os.path.join(data_directory, file_name)
    ranking_points = import_points(open_file(full_path))

    file_name = "Data/PRIZE MONEY.csv"
    full_path = os.path.join(data_directory, file_name)
    list_of_tournaments = import_tournaments(open_file(full_path),
                                             male_players, female_players)

    # Now have a circuit populated by players and tournaments, along with points and prize money
    return TournamentCircuit(list_of_tournaments, ranking_points,
                             male_players, female_players)


def open_file(file_name):
    # open file and store each row into a list
        try:
            # open using 'with' command closes file after everything is executed
            with open(file_name, "r") as csv_file:
                # delimit by comma because csv files
                file = csv.reader(csv_file, delimiter=',')
                file_row_list = list()
                # for each row in the csv, write to new file
                for row in file:
                    file_row_list.append(row)
                return file_row_list
        # exception catching
        except FileNotFoundError:
            print("No File with name {0}".format(file_name))
            return list()
        except IsADirectoryError:
            print("Is a directory not a file")
            return list()


# handles player import
def import_players(file_row_list):
    list_of_players = list()
    for row in file_row_list:
        list_of_players.append(Player(row[0]))
    return list_of_players


# handles points to be input
def import_points(file_row_list):
    points = dict()
    # get points from file
    for i in range(len(file_row_list) - 1, 0, -1):
        row = file_row_list[i]
        # only import unique values
        if row[0] in points.values():
            continue
        else:
            points[row[1]] = row[0]

    return points


# handles importing tournaments and prize money
def import_tournaments(file_row_list, male_players, female_players):
        q = Queue()
        s = Stack()
        temp = list()
        tournament_codes = list()
        list_of_tournaments = list()

        # loop through each row imported
        for row in file_row_list:
            for i in range(len(row)):
                # if row is tournament code
                if len(row[0]) > 0 and i == 0:
                    tournament_codes.append(row[0])
                # if row is empty
                if len(row[i]) == 0:
                    continue
                q.enqueue(row[i])
        # use this bool to not start adding to list until first tournament code
        # is found
        add_to_list = False
        # remove header from tournament codes
        # Sort data into lists
        for i in range(q.size()):
            # grabs current item at head of queue
            current_item = q.dequeue()
            # if item is not a tournament code but is a value add to temp list
            if add_to_list and current_item not in tournament_codes:
                temp.append(current_item)
            # if current item is a tournament code
            if current_item in tournament_codes:
                # add temp(tournament code and values for prize money) to list
                s.push(temp)
                # re-create empty list to add next load of values
                temp = list()
                # add tournament code to new list
                temp.append(current_item)
                # used to remove header
                add_to_list = True

        # push last code to stack
        s.push(temp)

        # loop through stack that holds lists with info about each tournament and
        # respective prize money allocations
        for i in range(s.size()):
            current = s.pop()
            if len(current) > 0:
                # get tournament code which is at start of list
                code = current.pop(0)
                # sort list values into dict of position ranked and money earned
                prize_money = dict()
                for j in range(len(current)):
                    if len(current) > 0:
                        position = current.pop(0)
                        money = current.pop(0)
                        money = money.replace(',', '')
                        # strip unwanted characters
                        # put tournament prize money into dictionary
                        prize_money[position] = money

                    else:
                        continue
                        
                # create new tournament object
                current_tournament = Tournament(code, prize_money, male_players, female_players)
                list_of_tournaments.append(current_tournament)
            else:
                continue

        # removes header from list
        list_of_tournaments.pop(len(list_of_tournaments) - 1)

        return list_of_tournaments


def update_overall_info_file(tournament_circuit, gender):

    if gender == "LADIES":
        list_of_players = tournament_circuit.female_circuit_players
    else:
        list_of_players = tournament_circuit.male_circuit_players

    info = list()

    # writing player's name
    for player in list_of_players:
        name = player.player_name
        points = str(player.ranking_points)
        money = str(player.prize_money)
        info.append(name)
        info.append(points)
        info.append(money)

    data_directory = os.path.dirname(__file__) + "/Data"
    file_name = "OVERALL {0} INFO".format(gender)
    write_to_file(info, data_directory, file_name)


def import_save_file(tournament_circuit):
    # import female player overall points and money

    info = open_file("Data/OVERALL LADIES INFO.csv")
    tournament_circuit.female_circuit_players = import_player_info(tournament_circuit.female_circuit_players,
                                                                   info)

    # same with male player info
    info = open_file("Data/OVERALL MEN INFO.csv")
    tournament_circuit.male_circuit_players = import_player_info(tournament_circuit.male_circuit_players,
                                                                 info)
    # Import Tournament info

    new_list_of_tournaments = list()

    for tournament in tournament_circuit.list_of_tournaments:
        file = "Data/{0} MEN INFO.csv".format(tournament.tournament_code)
        men_info = open_file(file)
        print(file)
        tournament = import_tournament_info(tournament, men_info, gender="0")
        file = "Data/{0} LADIES INFO.csv".format(tournament.tournament_code)
        women_info = open_file(file)
        print(file)
        tournament = import_tournament_info(tournament, women_info, gender="1")
        new_list_of_tournaments.append(tournament)
    print()
    tournament_circuit.list_of_tournaments = new_list_of_tournaments

    return tournament_circuit


def import_player_info(list_of_players, info):
    # while importing results, if file is empty, will not do anything to list of players
    while len(info) != 0 and len(info) > 3:
        name = info.pop(0)
        name = "".join(name)
        points = info.pop(0)
        points = "".join(points)
        money = info.pop(0)
        money = "".join(money)

        for player in list_of_players:
            if name == player.player_name:
                player.ranking_points += int(points)
                player.prize_money += int(money)

    return list_of_players


def import_tournament_info(current_tournament, info, gender):

    current_round = int(info[0][0])

    # converts round scores back into 2d array object, rather than list of strings

    if current_round == 0:
        if gender == "0":
            current_tournament.male_tournament_complete = True
            print("[{0}] Male Input: Complete".format(current_tournament.tournament_code))
            return current_tournament
        elif gender == "1":
            print("[{0}] Female Input: Complete".format(current_tournament.tournament_code))
            current_tournament.female_tournament_complete = True
            return current_tournament
    else:
        male_tournament_players = current_tournament.tournament_male_players
        female_tournament_players = current_tournament.tournament_female_players
        players_left_to_play = info[1]
        round_scores = info[2]
        tournament_points = info[3]
        tournament_money = info[4]
        user_input_choice = info[5]

        new_round_scores = list()
        for i, game in enumerate(round_scores):
            # strips quote marks from round scores
            matches = re.findall(r"\'(.+?)\'", game)
            if len(matches) != 0:
                new_game = [matches[0], matches[1], matches[2], matches[3]]
                new_round_scores.append(new_game)

        if gender == "0":
            # importing male tournament results
            print("[{0}] Male Input: In Progress".format(current_tournament.tournament_code))
            current_tournament.male_current_round = current_round
            current_tournament.male_players_left_to_play = players_left_to_play
            current_tournament.male_round_scores = new_round_scores
            male_tournament_players = import_tournament_values(tournament_points, male_tournament_players,
                                                               points=True)
            male_tournament_players = import_tournament_values(tournament_money, male_tournament_players,
                                                               points=False)
            current_tournament.tournament_male_players = male_tournament_players
            current_tournament.male_tournament_input_type = user_input_choice

            return current_tournament

        else:
            # importing female tournament results
            print("[{0}] Female Input: In Progress".format(current_tournament.tournament_code))
            current_tournament.female_current_round = current_round
            current_tournament.female_players_left_to_play = players_left_to_play
            current_tournament.female_round_scores = new_round_scores
            female_tournament_players = import_tournament_values(tournament_points, female_tournament_players,
                                                                 points=True)
            female_tournament_players = import_tournament_values(tournament_money, female_tournament_players,
                                                                 points=False)
            current_tournament.tournament_female_players = female_tournament_players
            current_tournament.female_tournament_input_type = user_input_choice

            return current_tournament


# can be used for assigning tournament money and points
def import_tournament_values(list_of_values, tournament_players, points):
    for i in range(int(len(list_of_values)/2)):
        name = list_of_values.pop(0)
        value = list_of_values.pop(0)
        for player in tournament_players:
            if name == player.player_name:
                if points:
                    player.current_tournament_points = int(value)
                else:
                    player.current_tournament_prize_money = int(value)
        list_of_values.insert(len(list_of_values), name)
        list_of_values.insert(len(list_of_values), value)

    return tournament_players


def initialize_info_files(list_of_tournaments):
    print("--Writing--\n")
    # placeholder values for data files
    write = [["1"], ["1"], ["1"], ["1"], ["1"], ["1"]]
    # initializing each file with placeholder values
    for tournament in list_of_tournaments:
        men = "Data/{0} MEN INFO".format(tournament.tournament_code)
        print(men)
        women = "Data/{0} LADIES INFO".format(tournament.tournament_code)
        print(women)
        write_to_file(write, os.path.dirname(__file__), men)
        write_to_file(write, os.path.dirname(__file__), women)

    men = "Data/OVERALL MEN INFO"
    women = "Data/OVERALL LADIES INFO"
    print(men)
    write_to_file("", os.path.dirname(__file__), men)
    print(women)
    write_to_file(write, os.path.dirname(__file__), women)

    print("\n--Data Files Initialised--\n")


# managing the first round results
def import_round_results(file_row_list):
    round_results = list()
    for row in file_row_list:
        round_results.append(row)
    # Remove Header from list
    round_results.pop(0)
    return round_results


# writing to files
def write_to_file(list_to_write, directory, name_of_file):
    # use 'with' command closes file after everything is executed
    # open file, write rows in list to file
    with open('{0}/{1}.csv'.format(directory, name_of_file), 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(list_to_write)
