import random
from collections import Counter, defaultdict
from itertools import count

from plot.draw_cuttings_v1 import draw_cuttings_v1


class GeneticAlgorithm:
    def __init__(self,
                 beam_length,
                 element_count,
                 element_lengths,
                 population_size=50,
                 generation_count=100,
                 crossover_probability=0.8,
                 mutation_probability=0.1,
                 selection_method="tournament"):

        self.beam_length = beam_length
        self.element_count = element_count
        self.element_lengths = element_lengths
        self.population_size = population_size
        self.generation_count = generation_count
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.selection_method = selection_method.lower()
        self.population = []
        self.crossed_population = []

    def __generate_cut_order(self):
        return random.sample(range(self.element_count), self.element_count)

    def initialize_population(self):
        """
        Initialize the population for the genetic algorithm.

        This method generates the initial population by creating random chromosomes, where each chromosome represents
        the cutting order of available elements.
        The genotype is essentially the chromosome, it's represent cutting pattern
        and the goal is to cut all the specified elements according to this order.

        :params:
        - self: The GeneticAlgorithm object.

        :return:
        - None
        :rtype:
        - None
        """
        for _ in range(self.population_size):
            self.population.append(self.__generate_cut_order())

    def __calculate_waste(self, cut_order):
        """
        Calculate waste and beam count for a given cutting pattern.

        The method calculates the waste and number of beams used based on a cutting pattern represented by the input
        cut_order. The cut_order defines the order in which elements are cut.

        Parameters:
        - cut_order: List representing the cutting order of elements.
          Type: list

        Returns:
        - Waste size.
          Type: int
        """
        remaining_elements_length = self.beam_length
        waste = 0

        for idx in cut_order:
            element_length = self.element_lengths[idx]
            if remaining_elements_length >= element_length:
                remaining_elements_length -= element_length
            else:
                waste += remaining_elements_length
                remaining_elements_length = self.beam_length
                remaining_elements_length -= element_length

        waste += remaining_elements_length
        return waste

    def __calculate_fitness(self, cut_order):
        """
        Calculate the fitness of a given cutting pattern.

        :param cut_order: Cutting pattern to evaluate.
        :type cut_order: list

        :return: Fitness value for the cutting pattern.
        :rtype: float
        """
        waste = self.__calculate_waste(cut_order)

        return 1.0 / (waste + 1e-10)

    def update_population(self):
        """
        Update the population by keeping the best 80% of cutting patterns.

        This method sorts the cutting patterns in the population based on their fitness values in descending order,
        and then keeps the best 80% of them.

        :return: None
        """
        sorted_population = sorted(self.population, key=self.__calculate_fitness, reverse=True)

        # Keep the best 80% of the population
        keep_count = int(0.8 * len(sorted_population))
        self.population = sorted_population[:keep_count]

    def select_parents(self, cut_orders):
        """
        Select parents for reproduction based on the specified selection method.

        This method acts as a wrapper for different parent selection methods, delegating the selection process to the
        corresponding method based on the specified selection method.

        Parameters:
        - cut_patterns: List of cutting orders.
          Type: list

        Returns:
        - List of two selected parents.
          Type: list
        """

        if self.selection_method == "tournament":
            return self.select_parents_tournament(cut_orders)
        elif self.selection_method == "roulette":
            return self.select_parents_roulette(cut_orders)
        elif self.selection_method == "rank":
            return self.select_parents_rank(cut_orders)
        else:
            raise ValueError("Unsupported selection method")

    def select_parents_tournament(self, cut_orders):
        """
        Selects two parents using tournament selection with consideration for cut patterns.

        :param cut_orders: List of cut patterns representing the genotypes of the population.
        :return: List of two parents selected using tournament selection.
        """

        selected_parents = []  # Initialize the list of selected parents
        tournament_size = int(len(self.population) * 0.1)  # Tournament size (10% of the population)

        for _ in range(2):  # Loop for selecting two parents
            while True:
                # Randomly select parent candidates from the list of cut patterns
                tournament_candidates = random.sample(cut_orders, tournament_size)

                # Find the tournament winner based on fitness values
                winner = max(tournament_candidates, key=self.__calculate_fitness)

                # Check if the winner has not been selected before
                if winner not in selected_parents:
                    # Add the winner to the list of selected parents and break out of the while loop
                    selected_parents.append(winner)
                    break

        return selected_parents

    def select_parents_roulette(self, cut_orders):
        """
        Selects two parents using roulette wheel selection with consideration for cut patterns.

        :return: List of two parents selected using roulette wheel selection.
        """

        selected_parents = []  # Initialize the list of selected parents
        total_fitness = sum(self.__calculate_fitness(pattern) for pattern in cut_orders)

        for _ in range(2):  # Loop for selecting two parents
            # Generate a random value between 0 and the total fitness
            random_value = random.uniform(0, total_fitness)

            cumulative_fitness = 0
            for cut_order in cut_orders:
                # Accumulate fitness values to find the selected cut pattern
                cumulative_fitness += self.__calculate_fitness(cut_order)

                # Check if the cumulative fitness exceeds the random value
                if cumulative_fitness >= random_value:
                    selected_parents.append(cut_order)
                    break

        return selected_parents

    def select_parents_rank(self, cut_orders):
        """
        Selects two parents using rank-based selection with consideration for cut orders.

        :return: List of two parents selected using rank-based selection.
        """

        selected_parents = []  # Initialize the list of selected parents

        # Sort cut patterns based on their fitness values
        sorted_cut_orders = sorted(cut_orders, key=self.__calculate_fitness)

        # Assign ranks to cut patterns based on their order after sorting
        ranks = list(range(1, len(cut_orders) + 1))

        total_ranks = sum(ranks)

        for _ in range(2):  # Loop for selecting two parents
            # Generate a random value between 0 and the total ranks
            random_value = random.uniform(0, total_ranks)

            cumulative_rank = 0
            for idx, cut_order in enumerate(sorted_cut_orders):
                # Accumulate ranks to find the selected cut pattern
                cumulative_rank += ranks[idx]

                # Check if the cumulative rank exceeds the random value
                if cumulative_rank >= random_value:
                    selected_parents.append(cut_order)
                    break

        return selected_parents

    def crossover(self):
        """
        Performs crossover operation on the population with a given crossover probability.

        For each individual in the population:
        - With a probability of crossover_probability, two parents are selected using the specified selection method.
        - A random crossover point is chosen.
        - Offspring are created by combining portions of the parents and filling the remaining elements based on order
        of the other parent.

        :return: None (Updates the population with crossed individuals).
        """

        for i in range(len(self.population)):
            # Check if crossover should be performed for the current individual
            if random.random() < self.crossover_probability:
                # Select two parents using the specified selection method
                parent1, parent2 = self.select_parents(self.population)

                # Choose a random crossover point
                crossover_point = random.randint(1, len(parent1) - 1)

                # Create offspring by combining portions of the parents
                child1 = parent1[:crossover_point] + [el for el in parent2 if el not in parent1[:crossover_point]]
                child2 = parent2[:crossover_point] + [el for el in parent1 if el not in parent2[:crossover_point]]

                # Add offspring to the crossed_population if not already present
                if child1 not in self.crossed_population:
                    self.crossed_population.append(child1)
                if child2 not in self.crossed_population:
                    self.crossed_population.append(child2)

    def combine_cut_orders(self):
        """
        Combines the current population with the crossed population, updating the overall population.

        The crossed population is emptied after the combination. Only unique individuals are retained, and the overall
        population is limited to the best individuals up to the population size.

        :return: None (Updates the population by extending it with the crossed population).
        """
        # Iterate through crossed population and add unique individuals to the overall population
        for individual in self.crossed_population:
            if individual not in self.population:
                self.population.append(individual)

        # Sort the combined population based on fitness values
        self.population = sorted(self.population, key=self.__calculate_fitness, reverse=True)

        # Keep only the best individuals up to the population size
        self.population = self.population[:self.population_size]

        # Empty the crossed population
        self.crossed_population = []

    def mutate(self):
        """
        Applies mutation to a set of cut patterns with a given mutation probability.

        For each cut pattern in the set:
        - With a probability of mutation_probability, two random elements are swapped.

        :return: List of mutated cut patterns.
        """
        modified_cut_orders = []
        for cut_order in self.population:
            # Check if mutation should be performed for the current cut pattern
            if random.random() < self.mutation_probability:
                # Choose two random indices for swapping
                idx1, idx2 = random.sample(range(len(cut_order)), 2)

                # Swap the elements at the selected indices
                cut_order[idx1], cut_order[idx2] = cut_order[idx2], cut_order[idx1]
            modified_cut_orders.append(cut_order)

        self.population = modified_cut_orders.copy()

    def choose_best(self):
        """
        Selects the best individual from the current population based on fitness values.

        :return: The individual with the highest fitness in the population.
        """
        return max(self.population, key=self.__calculate_fitness)

    def run(self):
        """
        Runs the genetic algorithm for a specified number of generations.

        The algorithm proceeds through the following steps in each generation:
        1. Initializes the population.
        2. Updates the population.
        3. Performs crossover operation.
        4. Applies mutation to the population.
        5. Repeats steps 2-4 for the specified number of generations.
        6. Returns the best individual from the final population.

        :return: The best individual from the final population after running the genetic algorithm.
        """
        # Step 1: Initialize the population
        self.initialize_population()

        # Steps 2-5: Iterate through the specified number of generations
        for _ in range(self.generation_count):
            # Step 2: Update the population
            self.update_population()

            # Step 3: Perform crossover operation
            self.crossover()

            self.combine_cut_orders()

            # Step 4: Apply mutation to the population
            self.mutate()

        # Step 6: Return the best individual from the final population
        return self.choose_best()

    def calculate_cut_patterns(self, cut_order):
        """
        Generates cut patterns for beams based on the given cut order, elements, and beam length.

        :param cut_order: List representing the order of elements to be cut.

        :return: List of cut patterns for each beam.
        """
        cut_patterns = []
        cut_pattern = []
        remaining_beam_length = self.beam_length

        for i in cut_order:
            if remaining_beam_length < self.element_lengths[i]:
                remaining_beam_length = self.beam_length
                cut_patterns.append(cut_pattern.copy())
                cut_pattern = []

            remaining_beam_length -= self.element_lengths[i]
            cut_pattern.append(self.element_lengths[i])

        cut_patterns.append(cut_pattern.copy())

        pattern_frequency = defaultdict(int)

        for cut_pattern in cut_patterns:
            sorted_pattern_tuple = tuple(sorted(cut_pattern, reverse=True))
            pattern_frequency[sorted_pattern_tuple] += 1

        return pattern_frequency

    def draw_cuttings(self, cut_patterns):
        draw_cuttings_v1(cut_patterns, self.beam_length)
