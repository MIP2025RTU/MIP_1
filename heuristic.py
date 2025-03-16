class Heuristic:
    @staticmethod
    def evaluate(current_number):
        """Method to return best move and respective score in current situation"""
        move1 = current_number * 2 # Multiply by 2 to get next number
        move2 = current_number * 3 # Multiply by 3 to get next number

        score1 = 1 if move1 % 2 == 0 else -1 #
        score2 = 1 if move2 % 2 == 0 else -1 # Evaluates results
        if score1 < score2:
            return score1, move1 # We return score1, move1 as the best, as score1 is lower than score2
        else:
            return score2, move2 # vice-versa, score2 is lower than score1 and it is being returned