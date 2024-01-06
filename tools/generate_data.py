import random

def generate_random_data():
    beam_length = random.randint(1000, 3000)

    element_count = random.randint(100, 200)

    unique_element_count = random.randint(5, 10)

    element_lengths = random.sample(range(10, 1000), unique_element_count)

    element_counts = []

    total_elements = 0
    for _ in range(unique_element_count):
        count = random.randint(1, max(1, (element_count - total_elements) // 4))
        total_elements += count
        element_counts.append(count)
    element_counts[unique_element_count-1] += (element_count - total_elements)

    data = [element for (frequency, element) in zip(element_counts, element_lengths) for _ in range(frequency)]
    random.shuffle(data)
    return beam_length, element_count, data
