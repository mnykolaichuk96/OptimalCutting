from collections import Counter

from tools.read_file import read_input_file

# Podana lista elementów
# element_lengths = [
#     210, 385, 875, 100, 230, 100, 210, 100, 100, 875,
#     230, 100, 100, 100, 385, 875, 210, 100, 230, 875,
#     210, 230, 385, 100, 210, 210, 875, 100, 385, 100,
#     875, 875, 210, 230, 100, 210, 875, 875, 210, 210,
#     100, 230, 100, 100, 875, 230, 385, 875, 210, 100,
#     100, 875, 385, 230, 100, 210, 210, 100, 385, 875,
#     100, 100, 875, 385, 230, 875, 100, 210, 230, 100,
#     100, 875, 210, 385, 100, 100, 100, 230, 875, 210,
#     100, 100, 100, 210, 875, 385, 230, 210, 100, 100,
#     100, 875, 385, 230, 210, 100, 100, 210, 230, 100,
#     100, 875, 875, 385, 100, 230, 875, 100, 100, 210,
#     210, 230, 100, 100, 875, 100, 385, 100, 875, 230,
#     210, 100, 100, 875, 210, 230, 100, 210, 100, 100,
#     875, 875, 385, 230, 100, 210, 100, 875, 385, 230,
#     100, 100, 210, 210, 875, 875, 100, 230, 100, 210
# ]
beam_length, element_count, element_lengths = read_input_file('data_10.txt')

# Użycie Counter do zliczenia wystąpień każdego elementu
zliczenia = Counter(element_lengths)

# Wyświetlenie wyników
for element, ilosc in zliczenia.items():
    print(f"Element {element}: {ilosc} razy")

