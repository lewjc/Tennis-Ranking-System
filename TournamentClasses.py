class TournamentCircuit:
    def __init__(self, list_of_tournaments, ranking_points,
                 male_circuit_players, female_circuit_players):

        self.list_of_tournaments = list_of_tournaments
        self.ranking_points = ranking_points
        self.male_circuit_players = male_circuit_players
        self.female_circuit_players = female_circuit_players


class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        self.prize_money = 0
        self.ranking_points = 0
        self.tournament_points = 0
        self.tournament_money = 0
        self.compare_overall_prize_money = False
        self.compare_overall_points = False

    # below are methods of comparison for the player objects, each one is determined by a boolean value.

    def __gt__(self, other):
        if self.compare_overall_points:
            if self.ranking_points > other.ranking_points:
                return True
            else:
                return False
        elif self.compare_overall_prize_money:
            if self.prize_money > other.prize_money:
                return True
            else:
                return False

        else:
            if self.tournament_points > other.tournament_points:
                return True
            else:
                return False

    def __lt__(self, other):
        if self.compare_overall_points:
            if self.ranking_points < other.ranking_points:
                return True
            else:
                return False
        elif self.compare_overall_prize_money:
            if self.prize_money < other.prize_money:
                return True
            else:
                return False
        else:
            if self.tournament_points < other.tournament_points:
                return True
            else:
                return False

    def __ge__(self, other):
        if self.compare_overall_points:
            if self.ranking_points >= other.ranking_points:
                return True
            else:
                return False
        elif self.compare_overall_prize_money:
            if self.prize_money >= other.prize_money:
                return True
            else:
                return False
        else:
            if self.tournament_points >= other.tournament_points:
                return True
            else:
                return False

    def __le__(self, other):
        if self.compare_overall_points:
            if self.ranking_points <= other.ranking_points:
                return True
            else:
                return False
        elif self.compare_overall_prize_money:
            if self.prize_money <= other.prize_money:
                return True
            else:
                return False
        else:
            if self.tournament_points <= other.tournament_points:
                return True
            else:
                return False

    # clear current tournament points

    def reset_tournament_points(self):
        self.tournament_points = 0

    def reset_tournament_money(self):
        self.tournament_money = 0


class Tournament:
    def __init__(self, tournament_code, prize_money_allocation,
                 tournament_male_players, tournament_female_players):

        self.tournament_code = tournament_code
        self.prize_money_allocation = prize_money_allocation
        self.tournament_difficulty = self.assign_tournament_difficulty()
        self.tournament_male_players = tournament_male_players
        self.tournament_female_players = tournament_female_players
        self.male_tournament_complete = False
        self.amount_of_rounds = self.set_amount_of_rounds()
        self.female_tournament_complete = False
        self.male_current_round = 1
        self.female_current_round = 1
        self.male_current_players_left_to_play = list()
        self.female_current_players_left_to_play = list()
        self.male_round_scores = list()
        self.female_round_scores = list()
        self.male_tournament_input_type = ""
        self.female_tournament_input_type = ""

    # determine tournament difficulty
    def assign_tournament_difficulty(self):
        if "TAC1" in self.tournament_code:
            return 2.7
        elif "TAE21" in self.tournament_code:
            return 2.3
        elif "TAW11" in self.tournament_code:
            return 3.1
        elif "TBS2"in self.tournament_code:
            return 3.25
        else:
            if self.tournament_code == "Tournament":
                return 0
            while True:
                try:
                    difficulty = float(input("Set {0} Difficulty (Between 1 & 5) :".format(self.tournament_code)))
                    if 1 <= difficulty <= 5:
                        return difficulty
                    else:
                        print("Incorrect Input")
                except ValueError:
                    print("Incorrect Input")

    def set_amount_of_rounds(self):
        i = len(self.tournament_male_players)
        r = 0
        while i != 1:
            i = i / 2
            r += 1
        return r
