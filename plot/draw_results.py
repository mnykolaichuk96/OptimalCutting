import matplotlib.pyplot as plt


def draw_results(x_list, y_list, x_label, y_label):
    # Tworzenie dwóch list z wynikami dla osi x i y
    x_values = []
    y_values = []

    for x, y in zip(x_list, y_list):
        x_values.append(x)
        y_values.append(y)

    # Rysowanie wykresu
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    plt.title(f'Stosunek {x_label.lower() } do {y_label.lower()}')
    plt.xlabel(x_label)
    if y_label == "Czas trwania":
        plt.ylabel(f'{y_label}, sek')
    else:
        plt.ylabel(y_label)
    plt.grid(True)
    plt.show()
