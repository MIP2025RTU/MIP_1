from heuristic import Heuristic

def test_heuristic():
    test_cases = [
        (5),   # Sāk ar 5 punktiem, jānovērtē labākais gājiens
        (13),  # Sāk ar 10 punktiem, spēlētājam ir 3 punkti
        (15), # Sāk ar 15 punktiem, spēlētājam ir -2 punkti
        (20),  # Sāk ar 20 punktiem, spēlētājam ir 5 punkti
    ]

    for current_number in test_cases:
        score = Heuristic.evaluate(current_number)[0]
        move = Heuristic.evaluate(current_number)[1]
        print(f"Skaitlis: {current_number}-> Heuristikas vērtējums: {score}")
        print(f"Skaitlis: {current_number}-> Izvēlētais skaitlis: {move}")

# Palaiž testu
test_heuristic()
