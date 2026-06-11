import random


def fitness(solution, items, capacity):
    bins = {}

    for i in range(len(solution)):
        b = solution[i]
        bins[b] = bins.get(b, 0) + items[i]

    penalty = sum(max(0, bins[b] - capacity) for b in bins)
    fill_score = sum((bins[b] / capacity) ** 2 for b in bins)

    return len(bins) + penalty * 20 - fill_score


def create_solution(num_items, max_bins):
    return [random.randint(0, max_bins - 1) for _ in range(num_items)]


def crossover(p1, p2):
    point = random.randint(0, len(p1) - 1)
    return p1[:point] + p2[point:]


def mutate(solution, max_bins):
    idx = random.randint(0, len(solution) - 1)
    solution[idx] = random.randint(0, max_bins - 1)
    return solution


def selection(population, items, capacity):
    population.sort(key=lambda x: fitness(x, items, capacity))
    return population[:len(population)//2]


def genetic_algorithm(items, capacity, generations=100, population_size=20):
    num_items = len(items)
    max_bins = num_items

    population = [create_solution(num_items, max_bins) for _ in range(population_size)]

    for _ in range(generations):
        selected = selection(population, items, capacity)

        new_population = selected.copy()

        while len(new_population) < population_size:
            p1 = random.choice(selected)
            p2 = random.choice(selected)

            child = crossover(p1, p2)
            child = mutate(child, max_bins)

            new_population.append(child)

        population = new_population

    return min(population, key=lambda x: fitness(x, items, capacity))