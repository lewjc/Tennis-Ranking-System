import FileManager
import os
import random
import QuickSort
import locale



def input_results(current_tournament, gender, ranking_points, input_from_file):
    locale.setlocale( locale.LC_ALL, '' )

    # directory is current  folder where file is
    file_dir = os.path.dirname(__file__)
    # get name of first round file, dependent on tournament code
    if gender == "LADIES":
        player_type = "1"
    else:
        player_type = "0"

    # Lists needed in function
    round_winners = list()
    players_to_write_to_file = list()
    players_left_to_play = list()
    tournament_difficulty = current_tournament.tournament_difficulty
    prize_money = current_tournament.prize_money_allocation

    # if men tournament
    if player_type == "0":
        # get current info for this tournament
        current_tournament_players = current_tournament.tournament_male_players
        user_input_choice = current_tournament.male_tournament_input_type
        current_round = current_tournament.male_current_round
        # if no previous results have been entered
        if current_round == 1 and len(current_tournament.male_current_players_left_to_play) == 0:
            for player in current_tournament_players:
                players_left_to_play.append(player.player_name)
            players_to_write_to_file = players_left_to_play

        else:
            players_left_to_play = current_tournament.male_players_left_to_play

    # if women tournament
    elif player_type == "1":
        current_tournament_players = current_tournament.tournament_female_players
        user_input_choice = current_tournament.female_tournament_input_type
        # check if we are on first round or higher, depending on if new circuit or not
        current_round = current_tournament.female_current_round
        # if no previous results have been entered
        if current_round == 1 and len(current_tournament.female_current_players_left_to_play) == 0:
            # populate players left to play with all players in tournament
            for player in current_tournament_players:
                players_left_to_play.append(player.player_name)
            players_to_write_to_file = players_left_to_play

        # if we have results that we have not yet finished entering, get current players left
        else:
            players_left_to_play = current_tournament.female_players_left_to_play

    # if not male or female (Shouldn't be possible)
    else:
        print("INVALID PLAYER TYPE")
        return

    # populates lists based on if swe are importing previous results or not

    if current_round == 1 and len(players_left_to_play) != 0:
        input_from_file = True
        all_player_tournament_points = list("0")
        all_player_tournament_money = list("0")
        # specify where we are going to write results to
        file_name = "Data/{0} ROUND 1 {1}.csv".format(current_tournament.tournament_code, gender)
        full_path = os.path.join(file_dir, file_name)

        # open file and return info as a list
        round_scores = FileManager.open_file(full_path)
        # removes initial value "1" stored in file when initialised
        if round_scores[0] == "1":
            round_scores.pop(0)
        # remove header
        round_scores.pop(0)
        # get games for the first round
        FileManager.import_round_results(round_scores)

    # if we are using previous results
    elif current_round > 1:
        all_player_tournament_points = list()
        all_player_tournament_money = list()
        round_scores = list()
        # determine whether or not user was inputting results from file
        if '1' in user_input_choice:
            input_from_file = False
        else:
            input_from_file = True

        # get current tournament money and points
        for player in current_tournament_players:

            if int(player.tournament_points) == 0:
                continue
            elif int(player.tournament_points) > 0:
                all_player_tournament_points.append(player.player_name)
                all_player_tournament_points.append(player.tournament_points)
            elif int(player.tournament_money) == 0:
                continue
            elif int(player.tournament_money()) > 0:
                all_player_tournament_points.append(player.player_name)
                all_player_tournament_points.append(player.tournament_money)


    prize_money_string = locale.currency(int(prize_money["1"]), grouping=True)

    # output tournament info
    print("=================================================================")
    print("\n[{0}] Players: {1} | Top Prize: ${2} | Difficulty: {3} \n".format(current_tournament.tournament_code,
                                                                           len(current_tournament_players),
                                                                           prize_money_string,
                                                                           tournament_difficulty))
    print("=================================================================\n")
    input("--Press ENTER to start--\n")
    # not allocating prise money until round 2
    allocate_prize_money = False

    # removes initial 1 written to start of file when initialising
    if len(players_left_to_play) > 0:
        if players_left_to_play[0] == "1":
            players_left_to_play.pop(0)

    # while we're entering results
    while current_round <= current_tournament.amount_of_rounds:
        if current_round == current_tournament.amount_of_rounds:
            print("--FINAL--\n")
        else:
            print("--ROUND {0}--\n".format(current_round))
        # if round scores have not yet finished being entered and we are inputting from file
        # sim new amount of rounds, with the players left to play in the round

        if current_round > 1 and len(players_left_to_play) != 0 and input_from_file:
            players_to_write_to_file = players_left_to_play
            if player_type == "0":
                round_scores = current_tournament.male_round_scores
            else:
                round_scores = current_tournament.female_round_scores

        # if current round has finished, add the round winners to players left to play
        elif current_round > 1 and len(players_left_to_play) == 0 and input_from_file:
            players_left_to_play = [player for player in round_winners]
            round_winners.clear()
            if len(round_scores) == 0:
                round_scores = simulate_tournament_results(players_left_to_play, player_type)

        # if user is inputting the results themselves, we have no need to do anything as it is up to the user
        # so we just write a 1 to the round scores file
        elif current_round > 1 and len(players_left_to_play) == 0 and not input_from_file:
            players_left_to_play = [player for player in round_winners]
            players_to_write_to_file = players_left_to_play
            round_scores = list("1")
            round_winners.clear()
        # if user is inputting results themselves however they left the program and there are still players left
        # to play then we need to assign round scores
        elif current_round > 1 and len(players_left_to_play) != 0 and not input_from_file:
            players_to_write_to_file = players_left_to_play
            round_scores = list("1")
        else:
            pass
        matches_to_write_to_file = round_scores

        # string of current round, players that haven't played in this round and the current scores
        info_string = [str(current_round), players_to_write_to_file, matches_to_write_to_file,
                       all_player_tournament_points, all_player_tournament_money, user_input_choice]
        # write to file, current round we are on and what players still need scores entered
        # for this round in case we exit, we can repopulate tournament with these values and carry on from
        # where we left off

        FileManager.write_to_file(info_string, file_dir, "Data/{0} {1} INFO".
                                  format(current_tournament.tournament_code, gender))

        # if prize money should be allocated
        if len(players_left_to_play) <= 16:
            allocate_prize_money = True
            # removes placeholder value in csv file
            if len(all_player_tournament_money) > 0:
                if all_player_tournament_money[0] == "0":
                    all_player_tournament_money.pop(0)

        # if there is still games left to play, use that value
        if len(round_scores) > 1:
            amount_of_games_to_play = int(len(round_scores))
        # if there are no games to play (i.e the user is inputting results themselves)
        # then we want to allow input for as many games as there are players to play thoses games
        else:
            amount_of_games_to_play = int(len(players_left_to_play)/2)
        # loop through each individual game
        for i in range(amount_of_games_to_play):
            if input_from_file:
                while True:
                    # get next game
                    game = round_scores[i]
                    player_one = game[0]
                    player_one_score = int(game[1])
                    player_two = game[2]
                    player_two_score = int(game[3])
                    # if game is valid then continue with evaluating winners
                    if ensure_valid_game_input(player_one, player_two, player_one_score,
                                               player_two_score, player_type, players_left_to_play):
                        input_from_file_game_done = False
                        break
                    # if there are no players left, break
                    elif players_left_to_play == 0:
                        input_from_file_game_done = False
                        break
                    # if the game has already been played, then we still need to add the winner to list of winners
                    else:
                        input_from_file_game_done = True
                        if who_won(player_one_score, player_two_score) == 1:
                            round_winners.append(player_one)
                        else:
                            round_winners.append(player_two)
                        break

                # game already done, get next game
                if input_from_file_game_done:
                    continue

            # user input scores manually
            else:
                print("--Players left to play in round {0}--\n".format(current_round))
                # prints all players that still need to play in this round, so user knows what
                # players still need to be input, may prevent accidental double entries.
                [print(player, end=" ") for player in players_left_to_play]
                print()

                while True:
                    player_one = input("\nEnter player name: ")
                    player_one_score = input("Enter player score: ")
                    player_two = input("Enter player name: ")
                    player_two_score = input("Enter player score: ")
                    # try and convert input to an integer, if the user has not input an int, ask for anther input
                    try:
                        # converts input to upper case, in case user did not.
                        # and removes any leading or ending spaces.
                        player_one = (player_one.upper()).strip()
                        player_two = (player_two.upper()).strip()
                        # convert scores to int for comparison
                        player_one_score = int(player_one_score)
                        player_two_score = int(player_two_score)
                    except ValueError:
                        print("--Invalid Data type for score, please use int--")
                        continue

                    # if there are no problems with the user input, break the loop and evaluate
                    if ensure_valid_game_input(player_one, player_two, player_one_score,
                                               player_two_score, player_type, players_left_to_play):
                        break
                    # if there is a problem, ask for input again
                    else:
                        continue
                input("\n--ENTER--\n")

            print("[Player]: {0} [Sets Won]: {1} [Player]: {2} [Sets Won]: {3}\n".format(player_one, player_one_score,
                                                                                         player_two, player_two_score))

            # remove both players from left to play because game is valid
            players_left_to_play.remove(player_one)
            players_left_to_play.remove(player_two)

            # player one wins
            if who_won(player_one_score, player_two_score) == 1:
                winner = player_one
            # player two wins
            elif who_won(player_one_score, player_two_score) == 2:
                winner = player_two
            else:
                # shouldn't be possible, so we return empty list
                print("--ERROR--")
                return list()
            print("--{0} wins!--\n".format(winner))
            # add prize money
            if allocate_prize_money:
                # assign current money based on round
                current_tournament_players, money = assign_tournament_money(winner, current_round,
                                                                            current_tournament,
                                                                            current_tournament_players)
                # remove player and points from all tournament points, then add again with new money
                if winner in all_player_tournament_money:
                    index = all_player_tournament_money.index(winner)
                    index = index+1
                    del all_player_tournament_money[index]
                    all_player_tournament_money.insert(index, money)
                else:
                    all_player_tournament_money.append(winner)
                    all_player_tournament_money.append(money)

            # adding points
            current_tournament_players, points = assign_tournament_points(winner, current_round,
                                                                          current_tournament_players,
                                                                          ranking_points)
            if winner in all_player_tournament_points:
                index = all_player_tournament_points.index(winner)
                index = index + 1
                del all_player_tournament_points[index]
                all_player_tournament_points.insert(index, points)
            else:
                all_player_tournament_points.append(winner)
                all_player_tournament_points.append(points)

            # writing the data to the file so if at any point we quit, it can be loaded back.
            players_to_write_to_file = [player for player in players_left_to_play]

            FileManager.write_to_file(info_string, file_dir,
                                      "Data/{0} {1} INFO".format(current_tournament.tournament_code,
                                                                 gender))

            if all_player_tournament_points[0] == "0":
                all_player_tournament_points.remove("0")

            round_winners.append(winner)

        # if round is finished
        if len(players_left_to_play) == 0 or amount_of_games_to_play == 0:
            FileManager.write_to_file(info_string, file_dir,
                                      "Data/{0} {1} INFO".format(current_tournament.tournament_code,
                                                                 gender))

            print("--Round {0} scores all entered--\n".format(current_round))
            # increase round and write the winners to file
            current_round += 1
            write_round_winners = round_winners

            # if we are on second round or above and need to simulate the round scores
            # also if we have not imported any previous results, otherwise, we need to
            # carry on importing results

            if 1 < current_round <= current_tournament.amount_of_rounds and len(players_left_to_play) == 0:
                players_left_to_play.clear()

                # default option for inputting results is input from file, so we write the new round scores
                round_scores = simulate_tournament_results(round_winners, player_type)
                matches_to_write_to_file = round_scores
                info_string = [str(current_round), write_round_winners, matches_to_write_to_file,
                               all_player_tournament_points, all_player_tournament_money, user_input_choice]
                FileManager.write_to_file(info_string, file_dir,
                                          "Data/{0} {1} INFO".format(current_tournament.tournament_code,
                                                                     gender))
                print("--Choose input choice for next round--")
                print("--[1] Input yourself--")
                print("--[2] Input from file--")
                while True:
                    user_input_choice = input("-> ")

                    # if user decides to input results themselves, we overwrite the file to reflect that
                    # and should the user quit before they have finished the results inputs,
                    if user_input_choice == "1":
                        input_from_file = False
                        matches_to_write_to_file.clear()
                        info_string = [str(current_round), write_round_winners, matches_to_write_to_file,
                                       all_player_tournament_points, all_player_tournament_money, user_input_choice]
                        FileManager.write_to_file(info_string, file_dir,
                                                  "Data/{0} {1} INFO".format(current_tournament.tournament_code,
                                                                             gender))
                        break
                    if user_input_choice == "2":
                        input_from_file = True
                        break
                    
                    else:
                        print("--Invalid Choice--")
                        continue

            # if we have not yet finished result input for the tournament
            if current_round != current_tournament.amount_of_rounds + 1:
                if player_type == "0":
                    # increase current round
                    current_tournament.male_current_round = current_round
                    # populate players left to play with the winners from the last round
                    current_tournament.male_players_left_to_play = round_winners
                    current_round = current_tournament.male_current_round
                elif player_type == "1":
                    current_tournament.female_current_round = current_round
                    current_tournament.female_players_left_to_play = round_winners
                    current_round = current_tournament.female_current_round

                while True and current_round <= 5:
                    print("\n--[1] To view current ranking points--")
                    print("--[2] To view current prize money--")
                    print("--[3] Return to menu--")
                    print("--[ENTER] to continue--")
                    user_input = input("-> ")
                
                    if user_input == "1":
                        print_current_points_ranking(current_tournament_players)
                        print("\n")
                        continue
                    elif user_input == "2":
                        print_current_prize_money_ranking(current_tournament_players)
                        print("\n")
                        continue
                    elif user_input == "3":
                        return list()
                    else:
                        print("\n")
                        break

            # if tournament is finished
            else:
                current_tournament_players = assign_overall_points(current_tournament_players, tournament_difficulty)
                current_tournament_players = assign_overall_prize_money(current_tournament_players)
                for player in current_tournament_players:
                    player.reset_tournament_points()
                    player.reset_tournament_money()

                if player_type == "0":
                    current_tournament.male_tournament_complete = True
                else:
                    current_tournament.female_tournament_complete = True

                FileManager.write_to_file("0", file_dir,
                                          "Data/{0} {1} INFO".format(current_tournament.tournament_code,
                                                                     gender))
                print("--Match results all input, returning to main menu--")
                print("======================================================\n")

                return current_tournament_players, True


def ensure_valid_game_input(player_one, player_two, player_one_score,
                            player_two_score, player_type, players_left_to_play,):

    # checks for double entries of both players (input from file)
    if player_one not in players_left_to_play and player_two not in players_left_to_play:
        print("{0} and {1} results entered".format(player_one, player_two))
        return False
    # ensure different player names
    elif player_one == player_two:
        print("Inputted player name twice")
        return False
    # make sure players need to play
    elif player_one not in players_left_to_play:
        print("--{0} results already entered--".format(player_one))
        return False
    elif player_two not in players_left_to_play:
        print("--{0} results already entered--".format(player_two))
        return False
    # make sure scores are valid for current tournament
    elif not check_score(player_one_score, player_type):
        print("--{0} score is not valid--".format(player_one))
        return False
    elif not check_score(player_two_score, player_type):
        print("--{0} score is not valid".format(player_two))
        return False
    # ensure someone wins
    elif not check_player_won(player_one_score, player_two_score, player_type):
        return False
    # ensure scores are not equal
    elif player_one_score == player_two_score:
        print("--Nobody won, score invalid--")
        return False
    # match is all ok
    else:
        return True


def check_player_won(player_one_score, player_two_score, player_type):
    if player_type == "0":
        if player_one_score != 3 and player_two_score != 3:
            print("--Neither player scored 3 sets--")
            # there might be an injury 

            return False
    else:
        if player_one_score != 2 and player_two_score != 2:
            print("--Neither player scored 2 sets--")
            # there might be an injury
            
            return False

    return True


# ensure scores are valid
def check_score(score, player_type):
    # playerType 0 male, 1 female
    if player_type == "0":
        # men's game max 3 sets
        if 0 <= int(score) < 4:
            return True
        else:
            return False
        # women's game max 2 sets
    elif player_type == "1":
        if 0 <= int(score) < 3:
            return True
        else:
            return False
    # if invalid player type, shouldn't be possible but here to catch
    # the error just in case
    else:
        print("--Invalid player type--")
        return False


# determines the winner of a game
def who_won(player_one_score, player_two_score):
    if int(player_one_score) > int(player_two_score):
        return 1
    elif int(player_one_score < player_two_score):
        return 2
    else:
        print("Nobody won")
        return 0


def simulate_tournament_results(list_of_players, gender_choice):
    list_of_scores_from_round = list()
    if gender_choice == "0":
        max_score = 3
    else:
        max_score = 2

    for i in range(int(len(list_of_players) / 2)):
        # remove first 2 players
        player_one = list_of_players.pop(0)
        player_two = list_of_players.pop(0)

        player_one_score = random.randrange(0, (max_score + 1))

        if player_one_score == max_score:
            player_two_score = random.randrange(0, max_score)
        else:
            player_two_score = max_score

        match = [player_one, str(player_one_score), player_two, str(player_two_score)]
        list_of_scores_from_round.append(match)

        # add players back to queue
        list_of_players.insert(len(list_of_players), player_one)
        list_of_players.insert(len(list_of_players), player_two)

    return list_of_scores_from_round


def assign_tournament_points(player, current_round, current_tournament_players, ranking_points):

    points = len(current_tournament_players)

    for i in range(current_round):
        points = int(points/2)

    for i, tournament_player in enumerate(current_tournament_players):
        if player in tournament_player.player_name:
            tournament_player.tournament_points = int(ranking_points[str(points)])
    return current_tournament_players, ranking_points[str(points)]


# assign tournament players prize money, people who make it into round 3 will be assigned money for that nand
# etc.
def assign_tournament_money(player, current_round, current_tournament, current_tournament_players):

    money = len(current_tournament_players)

    for i in range(current_round):
        money = int(money/2)

    money = str(money)
    prize_money_allocation = current_tournament.prize_money_allocation
    for tournament_player in current_tournament_players:
        if player == tournament_player.player_name:
            tournament_player.tournament_money = prize_money_allocation[money]

    return current_tournament_players, prize_money_allocation[money]


# when tournament is finished then we need to multiply each players points by the tournament difficulty
def assign_overall_points(current_tournament_players, tournament_difficulty):

    for player in current_tournament_players:
        points = int((float(player.tournament_points)*tournament_difficulty))
        player.ranking_points = int(player.ranking_points)
        player.ranking_points += points
    return current_tournament_players


# when tournament is finished then we need to assign everyone their overall prize money
def assign_overall_prize_money(current_tournament_players):

    for player in current_tournament_players:
        money = int(player.tournament_money)
        player.prize_money += money
    return current_tournament_players


# display prize money allocation for everyone currently playing in the tournament
def print_current_prize_money_ranking(list_of_players):
    list_of_players = QuickSort.sort(list_of_players)

    print("--Current Prize Money Rankings--")
    for i, player in enumerate(list_of_players):
        print("Name: {0} Prize Money: {1}".format(player.player_name, player.tournament_money))


def print_current_points_ranking(list_of_players):
    list_of_players = QuickSort.sort(list_of_players)

    print("--Current Tournament Rankings--")
    for i, player in enumerate(list_of_players):
        print("Name: {0} Points: {1}".format(player.player_name, player.tournament_points))


def determine_if_all_tournament_results_input(list_of_tournaments):

    for tournament in list_of_tournaments:
        male_complete = tournament.male_tournament_complete
        female_complete = tournament.female_tournament_complete

        if male_complete and female_complete:
            continue
        else:
            return False

    print("--All tournament results have been input--")
    return True
