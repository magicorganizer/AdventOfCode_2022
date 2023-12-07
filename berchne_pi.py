def calculate_pi(n_terms):
    approximation = 0
    for i in range(n_terms):
        approximation += ((-1) ** i) / (2 * i + 1)
    pi_approximation = 4 * approximation
    return pi_approximation

# Anzahl der Terme für die Näherung von π eingeben
n_terms = int(input("Geben Sie die Anzahl der Terme für die Näherung von π ein: "))

# π Näherung berechnen
approx_pi = calculate_pi(n_terms)

# Ergebnis ausgeben
print(f"Näherung von π mit {n_terms} Termen: {approx_pi}")
