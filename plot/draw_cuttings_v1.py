from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.cm as cm


def draw_cuttings_v1(pattern_frequency_dict, beam_length):

    unique_elements_length = set(element for key in pattern_frequency_dict.keys() for element in key)
    all_elements_length = sum(sum(elements) * frequency for elements, frequency in pattern_frequency_dict.items())
    beam_count = sum(frequency for pattern, frequency in pattern_frequency_dict.items())
    solution_waste = 0
    # Mapping from cut length to a unique color index
    cut_length_color = defaultdict(lambda: len(cut_length_color))
    # Rysowanie wykresu
    fig, ax = plt.subplots()
    cut_pattern = pattern_frequency_dict.keys()

    # Iteracja po każdym zestawie danych
    for i, (cut_pattern, cut_count) in enumerate(pattern_frequency_dict.items()):
        # Suma długości cięć
        # total_cut_length = sum([length * count for length, count in zip(unique_elements_length, data)])

        # Dodawanie prostokątów reprezentujących cięcia
        left = 0
        for j, cut_length in enumerate(cut_pattern):
            # for _ in range(cut_count):  # Uwzględnianie ilości wystąpień elementu
            color_index = cut_length_color[cut_length]
            color = cm.viridis(color_index / len(cut_length_color))  # Wybieranie koloru z palety
            ax.barh(y=i, width=cut_length, left=left, color=color, edgecolor='black', linewidth=0.5)

            # Dodawanie etykiety z długością elementu
            ax.text(left + cut_length / 2, i + 0.2, str(cut_length), ha='center', va='center', color='black',
                    fontsize=8)

            left += cut_length

        waste = beam_length - sum(cut_pattern)
        solution_waste += (waste * cut_count)

        # Dodanie prostokąta reprezentującego ilość odpadu
        ax.barh(y=i, width=waste, left=left, color='white', edgecolor='black', linewidth=0.5)

        # Dodanie etykiety z ilością odpadu
        ax.text(left + waste / 2, i + 0.2, str(waste), ha='center', va='center', color='black',
                fontsize=8)

    # Ustawienie wysokości
    ax.set_ylim([-0.5, len(pattern_frequency_dict) - 0.5])
    ax.set_yticks(range(len(pattern_frequency_dict)))
    ax.set_yticklabels([f'{frequency} x ' for frequency in pattern_frequency_dict.values()])

    ax.set_xlim([0, 1234])

    # Dodanie dodatkowego tekstu poniżej osi X
    ax.text(0.5, -0.095,
            f'Zużyto {beam_count} belek.\n'
            f'Łączna długość elementów: {all_elements_length}\n'
            f'Elementów surowca wykorzystano: {beam_count * beam_length} ({(100 * all_elements_length) / (beam_count * beam_length):.2f}%)',
            ha='center', va='center', transform=ax.transAxes)
    # Dodanie dodatkowego tekstu powyżej grafiki
    ax.text(0.5, 1.05, f'Łączna długość odpadów: {solution_waste}\n', ha='center', va='center', transform=ax.transAxes)

    # Zwiększenie rozmiaru okna wykresu
    fig.set_size_inches(10, 7)  # Możesz dostosować szerokość i wysokość według własnych potrzeb

    # Wyświetlenie wykresu
    plt.show()

    print(f'\nŁączna długość odpadów: {solution_waste}\n'
          f'Zużyto: {beam_count} belek.\n'
          f'Łączna długość elementów: {all_elements_length}\n'
          f'Elementów surowca wykorzystano: {beam_count * beam_length} ({(100 * all_elements_length) / (beam_count * beam_length):.2f}%)')
