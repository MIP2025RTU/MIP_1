class Node:
    def __init__(self, value, player1_score=0, player2_score=0, is_player1_turn=True):
        self.value = value  # Pašreizējais skaitlis
        self.player1_score = player1_score  # Punkti spēlētājam 1
        self.player2_score = player2_score  # Punkti spēlētājam 2
        self.is_player1_turn = is_player1_turn  # Kura spēlētāja gājiens
        self.children = []  # Saraksts ar iespējamiem nākamajiem stāvokļiem
    
    def add_child(self, child):
        self.children.append(child)  # Pievienot nākamo mezglu


class GameTree:
    def __init__(self, start_value):
        self.root = Node(start_value)  # Sākuma mezgls

    def build_tree(self, node):
        """ Rekursīvi izveido spēles koku """
        if node.value >= 1000:
            return  # Ja sasniedz 1000, beidzam
        
        for multiplier in [2, 3]:  # Divas iespējas: reizināt ar 2 vai 3
            new_value = node.value * multiplier
            new_p1_score = node.player1_score
            new_p2_score = node.player2_score

            # Punktu skaitīšanas noteikumi
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

            # Izveido jaunu mezglu un pievieno to kokam
            child = Node(new_value, new_p1_score, new_p2_score, not node.is_player1_turn)
            node.add_child(child)

            # Rekursīvi pievieno nākamos gājienus
            self.build_tree(child)

    def print_tree(self, node, depth=0):
        """ Izdrukā spēles koku """
        print("  " * depth + f"Value: {node.value}, P1: {node.player1_score}, P2: {node.player2_score}")
        for child in node.children:
            self.print_tree(child, depth + 1)


# Lietotājs ievada sākuma skaitli
start_number = int(input("Enter a starting number (5-15): "))

# Izveido spēles koku
game_tree = GameTree(start_number)
game_tree.build_tree(game_tree.root)

# Izdrukā izveidoto spēles koku
game_tree.print_tree(game_tree.root)
