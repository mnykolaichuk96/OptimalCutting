from algorithms import genetic_algorithm_v1
from algorithms import genetic_algorithm_v2
from plot.draw_results import draw_results
from tools.generate_data import generate_random_data
from tools.read_file import read_input_file
import time

# for i in range(1, 11):
#     data = generate_random_data()
#
#     with open(f'data_{i}.txt', 'w') as file:
#         file.write(str(data[0]) + '\n')
#         file.write(str(data[1]) + '\n')
#
#         for element_length in data[2]:
#             file.write(str(element_length) + '\n')

for i in range(5, 11, 1):
    beam_length, element_count, element_lengths = read_input_file(f'data_{i}.txt')

    # ga_v1 = genetic_algorithm_v1.GeneticAlgorithm(
    #     beam_length=beam_length,
    #     element_count=element_count,
    #     element_lengths=element_lengths,
    #     population_size=200,
    #     generation_count=15,
    #     crossover_probability=0.8,
    #     mutation_probability=0.2,
    #     selection_method="tournament"
    # )
    # best_solution_v1 = ga_v1.run()
    # cat_patterns = ga_v1.calculate_cut_patterns(best_solution_v1)
    # ga_v1.draw_cuttings(cat_patterns)

    best_params = []

    results = []
    for population_size in range(50, 251, 50):
        print(population_size)
        ga_v2 = genetic_algorithm_v2.GeneticAlgorithm(
            beam_length=beam_length,
            element_count=element_count,
            element_lengths=element_lengths,
            population_size=population_size,
        )

        best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned = ga_v2.run()

        results.append([
            genotype_waste,
            population_size,
        ])
        if population_size > population_size_returned:
            break

    best_params.append(min(results, key=lambda x: x[0])[1])

    results = []
    for generation_count in range(10, 26, 5):
        ga_v2 = genetic_algorithm_v2.GeneticAlgorithm(
            beam_length=beam_length,
            element_count=element_count,
            element_lengths=element_lengths,
            population_size=best_params[0],
            generation_count=generation_count,
        )

        best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned = ga_v2.run()

        results.append([
            genotype_waste,
            generation_count,
        ])

    best_params.append(min(results, key=lambda x: x[0])[1])

    results = []
    for next_generation_feasible_patterns_percent in [i / 100 for i in range(60, 101, 5)]:
        ga_v2 = genetic_algorithm_v2.GeneticAlgorithm(
            beam_length=beam_length,
            element_count=element_count,
            element_lengths=element_lengths,
            population_size=best_params[0],
            generation_count=best_params[1],
            next_generation_feasible_patterns_percent=next_generation_feasible_patterns_percent
        )

        best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned = ga_v2.run()

        results.append([
            genotype_waste,
            next_generation_feasible_patterns_percent,
        ])

    best_params.append(min(results, key=lambda x: x[0])[1])

    results = []
    for mutation_probability in [i / 100 for i in range(5, 101, 5)]:
        ga_v2 = genetic_algorithm_v2.GeneticAlgorithm(
            beam_length=beam_length,
            element_count=element_count,
            element_lengths=element_lengths,
            population_size=best_params[0],
            generation_count=best_params[1],
            next_generation_feasible_patterns_percent=best_params[2],
            mutation_probability=mutation_probability
        )

        best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned = ga_v2.run()

        results.append([
            genotype_waste,
            mutation_probability,
        ])

    best_params.append(min(results, key=lambda x: x[0])[1])

    print(f"Wzgłędnie najlepszy zestaw parametrów dla danych z zestawu {i}:", best_params)

    results = []
    for population_size in range(50, 251, 50):
        start_time = time.time()
        ga_v2 = genetic_algorithm_v2.GeneticAlgorithm(
            beam_length=beam_length,
            element_count=element_count,
            element_lengths=element_lengths,
            population_size=population_size,
            generation_count=best_params[1],
            next_generation_feasible_patterns_percent=best_params[2],
            mutation_probability=best_params[3]
        )

        best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned = ga_v2.run()

        end_time = time.time()
        elapsed_time = end_time - start_time

        results.append([
            genotype_waste,
            population_size,
            elapsed_time
        ])
        if population_size > population_size_returned:
            break

    draw_results([result[1]for result in results], [result[0]for result in results], "Rozmiar populacji", "Ilość odpadów")
    draw_results([result[1]for result in results], [result[2]for result in results], "Rozmiar populacji", "Czas trwania")

    results = []
    for generation_count in range(10, 26, 5):
        start_time = time.time()
        ga_v2 = genetic_algorithm_v2.GeneticAlgorithm(
            beam_length=beam_length,
            element_count=element_count,
            element_lengths=element_lengths,
            population_size=best_params[0],
            generation_count=generation_count,
            next_generation_feasible_patterns_percent=best_params[2],
            mutation_probability=best_params[3]
        )

        best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned = ga_v2.run()

        end_time = time.time()
        elapsed_time = end_time - start_time

        results.append([
            genotype_waste,
            generation_count,
            elapsed_time
        ])

    draw_results([result[1]for result in results], [result[0]for result in results], "Liczba generacji", "Ilość odpadów")
    draw_results([result[1]for result in results], [result[2]for result in results], "Liczba generacji", "Czas trwania")

    results = []
    for next_generation_feasible_patterns_percent in [i / 100 for i in range(60, 101, 5)]:
        start_time = time.time()
        ga_v2 = genetic_algorithm_v2.GeneticAlgorithm(
            beam_length=beam_length,
            element_count=element_count,
            element_lengths=element_lengths,
            population_size=best_params[0],
            generation_count=best_params[1],
            next_generation_feasible_patterns_percent=next_generation_feasible_patterns_percent,
            mutation_probability=best_params[3]
        )

        best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned = ga_v2.run()

        end_time = time.time()
        elapsed_time = end_time - start_time

        results.append([
            genotype_waste,
            next_generation_feasible_patterns_percent,
            elapsed_time
        ])

    draw_results([result[1]for result in results], [result[0]for result in results], "Procent najlepszych w kolejnych generacjach", "Ilość odpadów")
    draw_results([result[1]for result in results], [result[2]for result in results], "Procent najlepszych w kolejnych generacjach", "Czas trwania")

    results = []
    for mutation_probability in [i / 100 for i in range(5, 101, 5)]:
        start_time = time.time()
        ga_v2 = genetic_algorithm_v2.GeneticAlgorithm(
            beam_length=beam_length,
            element_count=element_count,
            element_lengths=element_lengths,
            population_size=best_params[0],
            generation_count=best_params[1],
            next_generation_feasible_patterns_percent=best_params[2],
            mutation_probability=mutation_probability
        )

        best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned = ga_v2.run()

        end_time = time.time()
        elapsed_time = end_time - start_time

        results.append([
            genotype_waste,
            mutation_probability,
            elapsed_time
        ])

    draw_results([result[1]for result in results], [result[0]for result in results], "Prowdopodobieństwo mutacji", "Ilość odpadów")
    draw_results([result[1]for result in results], [result[2]for result in results], "Prowdopodobieństwo mutacji", "Czas trwania")

    results_for_representation = []
    for _ in range(10):
        ga_v2 = genetic_algorithm_v2.GeneticAlgorithm(
            beam_length=beam_length,
            element_count=element_count,
            element_lengths=element_lengths,
            population_size=best_params[0],
            generation_count=best_params[1],
            next_generation_feasible_patterns_percent=best_params[2],
            mutation_probability=best_params[3]
        )
        best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned = ga_v2.run()
        results_for_representation.append(
            [best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned])

    best_solution, cutting_patterns_for_best_solution, genotype_waste, population_size_returned = (
        min(results_for_representation, key=lambda x: (x[2], len(x[0]))))

    ga_v2.draw_cuttings(best_solution, cutting_patterns_for_best_solution, genotype_waste)
