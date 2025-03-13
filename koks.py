# Katra mezgla (Node) definēšana spēles kokā
class Node:
    def __init__(self, value, player1_score=0, player2_score=0, is_player1_turn=True):
        # Mezglā esošais skaitlis (pašreizējā spēles vērtība)
        self.value = value  
        # Spēlētāja 1 punktu skaits
        self.player1_score = player1_score  
        # Spēlētāja 2 punktu skaits
        self.player2_score = player2_score  
        # Pārbauda, vai ir spēlētāja 1 gājiens (True - P1, False - P2)
        self.is_player1_turn = is_player1_turn  
        # Saraksts, kas saglabās visus iespējamos nākamos stāvokļus (bērnu mezglus)
        self.children = []  

    # Pievieno bērnu mezglu pašreizējam mezglam
    def add_child(self, child):
        self.children.append(child)  


# Spēles koka struktūra un darbība
class GameTree:
    def __init__(self, start_value):
        # Izveido saknes mezglu ar sākuma skaitli
        self.root = Node(start_value)  

    # Funkcija, kas rekursīvi izveido spēles koku
    def build_tree(self, node):
        """ Rekursīvi izveido spēles koku ar iespējamajiem gājieniem """
        # Ja skaitlis sasniedz vai pārsniedz 1000, pārtrauc koka veidošanu
        if node.value >= 1000:
            return  

        # Katrs spēlētājs var reizināt ar 2 vai 3
        for multiplier in [2, 3]:  
            # Aprēķina jauno skaitli
            new_value = node.value * multiplier  
            # Kopē spēlētāju punktu skaitu no iepriekšējā mezgla
            new_p1_score = node.player1_score  
            new_p2_score = node.player2_score  

            # Punktu piešķiršanas noteikumi atkarībā no tā, vai jaunais skaitlis ir pāra vai nepāra
            if new_value % 2 == 0:  # Ja pāra skaitlis
                if node.is_player1_turn:
                    new_p1_score += 1  # Spēlētājam 1 tiek pievienots punkts
                else:
                    new_p2_score += 1  # Spēlētājam 2 tiek pievienots punkts
            else:  # Ja nepāra skaitlis
                if node.is_player1_turn:
                    new_p1_score -= 1  # Spēlētājam 1 tiek atņemts punkts
                else:
                    new_p2_score -= 1  # Spēlētājam 2 tiek atņemts punkts

            # Izveido jaunu mezglu ar aprēķinātajiem datiem
            child = Node(new_value, new_p1_score, new_p2_score, not node.is_player1_turn)
            # Pievieno šo mezglu kā bērnu pašreizējam mezglam
            node.add_child(child)  

            # Rekursīvi turpina veidot spēles koku
            self.build_tree(child)  

    # Funkcija, kas izdrukā spēles koku
    def print_tree(self, node, depth=0):
        """ Rekursīvi izdrukā spēles koku ar atkāpēm, lai parādītu hierarhiju """
        print("  " * depth + f"Value: {node.value}, P1: {node.player1_score}, P2: {node.player2_score}")
        # Izsauc rekursīvu funkciju katram bērna mezglam, palielinot atkāpi
        for child in node.children:
            self.print_tree(child, depth + 1)  

    # Funkcija, kas izpilda interaktīvu spēli
    def play_game(self):
        """ Interaktīva spēle starp spēlētāju un datoru """
        current_node = self.root  # Sākam no saknes mezgla

        # Spēle turpinās, kamēr skaitlis nesasniedz vai nepārsniedz 1000
        while current_node.value < 1000:
            print(f"Current number: {current_node.value}")
            print(f"Player 1 Score: {current_node.player1_score}, Player 2 Score: {current_node.player2_score}")

            # Ja ir spēlētāja 1 gājiens, viņš izvēlas reizinātāju
            if current_node.is_player1_turn:
                choice = int(input("Choose multiplier (2 or 3): "))  
            else:
                # Dators nejauši izvēlas reizinātāju (2 vai 3)
                import random
                choice = random.choice([2, 3])  
                print(f"Computer chose: {choice}")

            # Aprēķina jauno skaitli un saglabā spēlētāju punktus
            new_value = current_node.value * choice
            new_p1_score = current_node.player1_score
            new_p2_score = current_node.player2_score

            # Jaunā skaitļa punktu piešķiršanas noteikumi
            if new_value % 2 == 0:  # Ja pāra skaitlis
                if current_node.is_player1_turn:
                    new_p1_score += 1  # Spēlētājam 1 tiek pievienots punkts
                else:
                    new_p2_score += 1  # Spēlētājam 2 tiek pievienots punkts
            else:  # Ja nepāra skaitlis
                if current_node.is_player1_turn:
                    new_p1_score -= 1  # Spēlētājam 1 tiek atņemts punkts
                else:
                    new_p2_score -= 1  # Spēlētājam 2 tiek atņemts punkts

            # Pāriet uz jaunu spēles stāvokli, izveidojot jaunu mezglu
            current_node = Node(new_value, new_p1_score, new_p2_score, not current_node.is_player1_turn)

        # Spēle beigusies – izdrukā gala rezultātus
        print(f"Final number: {current_node.value}")
        print(f"Final Scores -> Player 1: {current_node.player1_score}, Player 2: {current_node.player2_score}")

        # Nosaka uzvarētāju
        if current_node.player1_score < current_node.player2_score:
            print("Player 1 wins!")  
        elif current_node.player1_score > current_node.player2_score:
            print("Player 2 wins!")  
        else:
            print("It's a tie!")  # Ja punktu skaits ir vienāds, ir neizšķirts


# Lietotājs ievada sākuma skaitli, un tiek izveidots spēles koks
game_tree = GameTree(int(input("Enter a starting number (5-15): ")))
# Palaiž spēli, sākot no izveidotā koka saknes
game_tree.play_game()
