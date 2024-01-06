def read_input_file(file_path):
    with open(file_path, 'r') as file:
        beam_length = int(file.readline().strip())
        num_elements = int(file.readline().strip())
        element_lengths = [int(file.readline().strip()) for _ in range(num_elements)]

    return beam_length, num_elements, element_lengths