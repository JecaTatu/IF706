import random
import math

POPULATION_SIZE = 100
MUTATION_PROB = 0.4
RECOMBINATION_PROB = 0.9
EVALUATIONS_NUMBER = 10000
CHILDREN_NUMBER = 2

class Queens8:
    def __init__(self):
        self.best_solution = [0, 0, 0, 0, 0, 0, 0, 0]
        self.evaluations = 0
        self.population = self.generate_population()
        self.fitnesses = self.fitness(self.population)

    def run(self):
        maxFit = max(self.fitnesses)
        if math.isclose(maxFit, 1):
            print("############# SOLUÇÃO ENCONTRADA NA GERAÇÃO INICIAL #############")
            self.best_solution = self.population[self.fitnesses.index(1)]
            return
            
        while self.evaluations < EVALUATIONS_NUMBER:
            print("############# COMEÇO DA AVALIAÇÃO {} #############".format(self.evaluations))

            parents = self.parentSelection()
            children = self.recombination(parents)
            children = self.mutation(children)
            children_fitness = self.fitness(children)

            self.population = self.survivors(self.population + children, self.fitnesses + children_fitness)

            children_max_fit = max(children_fitness)
            if math.isclose(children_max_fit, 1):
                print("############# SOLUÇÃO ENCONTRADA NA AVALIAÇÃO {} #############".format(self.evaluations))
                child_index = children_fitness.index(children_max_fit)
                self.best_solution = children[child_index]
                return

            print("############# FIM DA AVALIAÇÃO {} #############".format(self.evaluations))

        self.best_solution = self.population[self.fitnesses.index(max(self.fitnesses))]
        print(max(self.fitnesses))

    def generate_population(self):
        population = []

        while len(population) < POPULATION_SIZE:
            genes = random.sample(range(8), 8)
            # if genes not in population:
            population.append(genes)

        return population

    def fitness(self, individuals):
        fitness_list = []
        for individual in individuals:
            self.evaluations += 1
            collisions = 0
            for idx in range(len(individual)):
                aux = 0
                for chk in range(idx, len(individual)):
                    if individual[chk] == individual[idx] + aux and idx != chk:
                        collisions += 1
                    elif individual[chk] == individual[idx] - aux and idx != chk:
                        collisions += 1
                    elif individual[chk] == individual[idx] and idx != chk:
                        collisions += 1
                    aux += 1
            fitness_list.append(1 / (1 + collisions))

        return fitness_list

    def mutation(self, individuals):
        for individual in individuals:
            if random.random() <= MUTATION_PROB:
                geneX = random.randint(0, len(individual) - 1)
                geneY = random.randint(0, len(individual) - 1)

                aux = individual[geneX]
                individual[geneX] = individual[geneY]
                individual[geneY] = aux
            
        return individuals

    def recombination(self, parents):
            if random.random() <= RECOMBINATION_PROB:
                parent_1 = parents[0]
                parent_2 = parents[1]

                cutPoint = random.randint(0, 7)
                
                children = []
                children.append(parent_1[:cutPoint] + parent_2[cutPoint:])
                children.append(parent_2[:cutPoint] + parent_1[cutPoint:])
                return children

            return parents


    def survivors(self, population, fitnesses):       
        while(len(population) > POPULATION_SIZE):
            del(population[fitnesses.index(min(fitnesses))])
            del(fitnesses[fitnesses.index(min(fitnesses))])
                    
        return population

    def parentSelection(self):
        parents_indexes = random.sample(range(len(self.population) - 1), 2)
        parents = [self.population[x] for x in parents_indexes]
        parents_fit = [self.fitnesses[x] for x in parents_indexes]

        choosens = []
        choosens.append(parents[parents_fit.index(max(parents_fit))])
        del(parents_fit[parents_fit.index(max(parents_fit))])
        choosens.append(parents[parents_fit.index(max(parents_fit))])

        return choosens

        
if __name__ == '__main__':
    queens8 = Queens8()
    queens8.run()
    print(queens8.best_solution)
