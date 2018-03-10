import Menu
import FileManager
import TournamentManager
import Leaderboard
import os

tournament_circuit = None

while True:
    user_choice = Menu.start_menu()

    if user_choice == "1":
        # create our circuit
        tournament_circuit = Menu.circuit_population_menu(FileManager.get_main_data())

        tournament_circuit
                
        tournament_codes = [tournament.tournament_code for tournament in
                            tournament_circuit.list_of_tournaments]
        FileManager.write_to_file(tournament_codes, os.path.dirname(os.path.abspath(__file__)),
                                  "Data/TOURNAMENTS IN CIRCUIT")
        FileManager.initialize_info_files(tournament_circuit.list_of_tournaments)
    elif user_choice == "2":
        # import main data
        tournament_circuit = FileManager.get_main_data()
        # populate main data with existing data about points, money and results.
        codes_in_circuit = FileManager.open_file(os.path.join(os.path.dirname(__file__),
                                                              "Data/TOURNAMENTS IN CIRCUIT.csv"))
        codes = ["".join(code) for code in codes_in_circuit]
        current_tournaments = [tournament for code in codes for tournament in
                               tournament_circuit.list_of_tournaments
                               if tournament.tournament_code == code]

        tournament_circuit.list_of_tournaments = current_tournaments
        tournament_circuit = FileManager.import_save_file(tournament_circuit)

    # start main menu
    while True:
        user_choice = Menu.main_menu()
        gender = None
        # input scores
        if user_choice == "1":
            while True:
                if TournamentManager.determine_if_all_tournament_results_input(tournament_circuit.list_of_tournaments):
                    while True:
                        choice = Menu.final_menu()
                        if choice == "1":
                            gender = Menu.choose_gender(0)
                            tournament_circuit = Leaderboard.display_overall_points_leaderboard(gender,
                                                                                                tournament_circuit)
                        else:
                            gender = Menu.choose_gender(0)
                            tournament_circuit = Leaderboard.display_overall_money_leaderboard(gender,
                                                                                               tournament_circuit)

                # get current tournament to input results for
                current_tournament = Menu.choose_tournament(tournament_circuit)
                if current_tournament == 0:
                    break

                gender = Menu.choose_gender(current_tournament)
                if gender == 0:
                    continue
                break
                
            if current_tournament == 0:
                continue
            results = TournamentManager.input_results(current_tournament, gender,
                                                      tournament_circuit.ranking_points, True)
            # if empty list is returned continue with menu (occurs when error occurs when importing file)
            if len(results) == 0:
                continue
            tournament_players = results
            FileManager.update_overall_info_file(tournament_circuit, gender)
            continue

        # display points ranking table
        elif user_choice == "2":
            # pass through zero as choose_gender usually takes a current tournament
            # 0 means just return a 0 or 1 based on the gender leader board the user wants to see
            gender = Menu.choose_gender(0)
            tournament_circuit = Leaderboard.display_overall_points_leaderboard(gender, tournament_circuit)
            continue
        # display money ranking table
        elif user_choice == "3":
            gender = Menu.choose_gender(0)
            tournament_circuit = Leaderboard.display_overall_money_leaderboard(gender, tournament_circuit)
            continue
    
        #added this

        # return to previous menu
        elif user_choice == "4":
            break
        else:
            print("Invalid Choice")
