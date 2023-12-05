# import random
#
#
# def approximate_pi(n):
#     points_inside_circle = 0
#     points_total = n
#
#     for i in range(n):
#         x = random.uniform(-1, 1)
#         y = random.uniform(-1, 1)
#         if x ** 2 + y ** 2 <= 1:
#             points_inside_circle += 1
#
#     return 4 * points_inside_circle / points_total
#
#
# print(approximate_pi(1000000))

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
