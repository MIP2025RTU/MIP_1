from heuristic import Heuristic

def test_heuristic():
    test_cases = [
        (5, 0),   # Sāk ar 5 punktiem, jānovērtē labākais gājiens
        (13, 0),  # Sāk ar 10 punktiem, spēlētājam ir 3 punkti
        (15, -2), # Sāk ar 15 punktiem, spēlētājam ir -2 punkti
        (20, 5),  # Sāk ar 20 punktiem, spēlētājam ir 5 punkti
    ]

    for current_number, player_score in test_cases:
        score = Heuristic.evaluate(current_number)[0]
        move = Heuristic.evaluate(current_number)[1]
        print(f"Skaitlis: {current_number}, Punkti: {player_score} -> Heuristikas vērtējums: {score}")
        print(f"Skaitlis: {current_number}, Punkti: {player_score} -> Izvēlētais skaitlis: {move}")

# Palaiž testu
test_heuristic()
