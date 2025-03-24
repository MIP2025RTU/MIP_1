import tkinter as tk
import random

class Node:
    def __init__(self, value, player1_score=0, player2_score=0, is_player1_turn=True):
        self.value = value
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.is_player1_turn = is_player1_turn
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class Heuristic:
    @staticmethod
    def evaluate(current_number):
        move1 = current_number * 2
        move2 = current_number * 3

        score1 = 1 if move1 % 2 == 0 else -1
        score2 = 1 if move2 % 2 == 0 else -1
        if score1 < score2:
            return score1, move1
        else:
            return score2, move2

class GameTree:
    def __init__(self, start_value):
        self.root = Node(start_value)

    def build_tree(self, node):
        if node.value >= 1000:
            return

        for multiplier in [2, 3]:
            new_value = node.value * multiplier
            new_p1_score = node.player1_score
            new_p2_score = node.player2_score

            if new_value % 2 == 0:
                if node.is_player1_turn:
                    new_p1_score += 1
                else:
                    new_p2_score += 1
            else:
                if node.is_player1_turn:
                    new_p1_score -= 1
                else:
                    new_p2_score -= 1

            child = Node(new_value, new_p1_score, new_p2_score, not node.is_player1_turn)
            node.add_child(child)
            self.build_tree(child)

    def best_move(self, node, depth, use_minimax=False):
        best_value = float('-inf')
        best_choice = None

        for child in node.children:
            if use_minimax:
                value = self.minimax(child, depth - 1, False)
            else:
                value = self.alpha_beta(child, depth - 1, float('-inf'), float('inf'), False)

            if node.is_player1_turn:
                value = child.player1_score - child.player2_score
            else:
                value = child.player2_score - child.player1_score

            if value > best_value:
                best_value = value
                best_choice = child

        return best_choice

    def minimax(self, node, depth, maximizingPlayer):
        if node.value >= 1000 or depth == 0:
            return self.heuristic_evaluation(node)

        if maximizingPlayer:
            max_eval = float('-inf')
            for child in node.children:
                eval = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.children:
                eval = self.minimax(child, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def heuristic_evaluation(self, node):
        score, _ = Heuristic.evaluate(node.value)
        return score

    def alpha_beta(self, node, depth, alpha, beta, maximizingPlayer):
        if node.value >= 1000 or depth == 0:
            return self.heuristic_evaluation(node)

        if maximizingPlayer:
            max_eval = float('-inf')
            for child in node.children:
                eval = self.alpha_beta(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.children:
                eval = self.alpha_beta(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spēle: Minimaksa vs Alfa-beta")

        self.start_label = tk.Label(root, text="Ievadiet sākuma skaitli (5-15):")
        self.start_label.pack()
        self.start_entry = tk.Entry(root)
        self.start_entry.pack()

        self.player_label = tk.Label(root, text="Kurš sāk spēli? (cilvēks/dators)")
        self.player_label.pack()
        self.player_choice = tk.StringVar(value="cilvēks")
        self.player_menu = tk.OptionMenu(root, self.player_choice, "cilvēks", "dators")
        self.player_menu.pack()

        self.algo_label = tk.Label(root, text="Izvēlieties algoritmu (minimaksa/alfa-beta)")
        self.algo_label.pack()
        self.algo_choice = tk.StringVar(value="alfa-beta")
        self.algo_menu = tk.OptionMenu(root, self.algo_choice, "minimaksa", "alfa-beta")
        self.algo_menu.pack()

        self.start_button = tk.Button(root, text="Sākt spēli", command=self.start_game)
        self.start_button.pack()

        self.output_label = tk.Label(root, text="", font=("Arial", 12))
        self.output_label.pack()

        self.points_label = tk.Label(root, text="Cilvēka punkti: 0 | Datora punkti: 0", font=("Arial", 12))
        self.points_label.pack()

        self.move_entry = tk.Entry(root)
        self.move_button = tk.Button(root, text="Veikt gājienu", command=self.player_move)

        self.current_node = None
        self.tree = None

    def start_game(self):
        try:
            start_value = int(self.start_entry.get())
            if not (5 <= start_value <= 15):
                raise ValueError
        except ValueError:
            self.output_label.config(text="Lūdzu, ievadiet skaitli no 5 līdz 15")
            return

        self.tree = GameTree(start_value)
        self.tree.build_tree(self.tree.root)
        self.current_node = self.tree.root

        self.update_gui()

        if self.player_choice.get() == "cilvēks":
            self.move_entry.pack()
            self.move_button.pack()
        else:
            self.root.after(1000, self.ai_move)

    def player_move(self):
        try:
            choice = int(self.move_entry.get())
            if choice not in [2, 3]:
                raise ValueError
        except ValueError:
            self.output_label.config(text="Lūdzu, ievadiet 2 vai 3")
            return

        self.apply_move(choice)
        self.update_gui()

        if self.current_node.value < 1000:
            self.root.after(1000, self.ai_move)
        else:
            self.end_game()

    def ai_move(self):
        remaining_steps = (1000 - self.current_node.value) // 2
        depth = min(max(4, remaining_steps), 6)

        use_minimax = self.algo_choice.get() == "minimaksa"
        best_move = self.tree.best_move(self.current_node, depth, use_minimax=use_minimax)

        if best_move is not None:
            if best_move.value == self.current_node.value * 2:
                choice = 2
            else:
                choice = 3
        else:
            choice = random.choice([2, 3])

        self.apply_move(choice)
        self.update_gui()

        if self.current_node.value >= 1000:
            self.end_game()
        else:
            self.move_entry.pack()
            self.move_button.pack()

    def apply_move(self, multiplier):
        new_value = self.current_node.value * multiplier
        p1 = self.current_node.player1_score
        p2 = self.current_node.player2_score
        turn = not self.current_node.is_player1_turn

        if new_value % 2 == 0:
            if self.current_node.is_player1_turn:
                p1 += 1
            else:
                p2 += 1
        else:
            if self.current_node.is_player1_turn:
                p1 -= 1
            else:
                p2 -= 1

        self.current_node = Node(new_value, p1, p2, turn)

    def update_gui(self):
        self.output_label.config(text=f"Pašreizējais skaitlis: {self.current_node.value}")
        self.points_label.config(text=f"Cilvēka punkti: {self.current_node.player1_score} | Datora punkti: {self.current_node.player2_score}")

    def end_game(self):
        if self.current_node.player1_score < self.current_node.player2_score:
            result = "Cilvēks uzvarēja!"
        elif self.current_node.player1_score > self.current_node.player2_score:
            result = "Dators uzvarēja!"
        else:
            result = "Neizšķirts!"

        self.output_label.config(text=f"Spēle beigusies! {result} Iegūtais skaitlis: {self.current_node.value}")
        self.move_entry.pack_forget()
        self.move_button.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    gui = GameGUI(root)
    root.mainloop()