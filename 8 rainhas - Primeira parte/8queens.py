import random
import math
import bitstring

POPULATION_SIZE = 100
MUTATION_PROB = 0.4
RECOMBINATION_PROB = 0.9
EVALUATIONS_NUMBER = 10000
CHILDREN_NUMBER = 2
CHROMOSOME_GENES = 8
GENE_SIZE = 3

class Queens8:
    def __init__(self):
        self.best_solution = bitstring.BitArray(bin='')
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

    def decode_chromosome(self, chromosome):
        positions = []
        for i in range(CHROMOSOME_GENES):
            position = int(chromosome.bin[3 * i:(i + 1) * GENE_SIZE], 2)
            positions.append(position)

        return positions

    def generate_population(self):
        population = []

        while len(population) < POPULATION_SIZE:
            decoded_genes = random.sample(range(CHROMOSOME_GENES), CHROMOSOME_GENES)
            
            genes = "0b"
            for gene in decoded_genes:
                genes += format(gene, "0" + str(GENE_SIZE) + "b")
            genes = bitstring.BitArray(genes)
            # if genes not in population:
            population.append(genes)

        return population

    def fitness(self, individuals):
        fitness_list = []
        for individual in individuals:
            positions = self.decode_chromosome(individual)
            self.evaluations += 1
            collisions = 0
            for idx in range(len(positions)):
                aux = 0
                for chk in range(idx, len(positions)):
                    if positions[chk] == positions[idx] + aux and idx != chk:
                        collisions += 1
                    elif positions[chk] == positions[idx] - aux and idx != chk:
                        collisions += 1
                    elif positions[chk] == positions[idx] and idx != chk:
                        collisions += 1
                    aux += 1
            fitness_list.append(1 / (1 + collisions))

        return fitness_list

    def mutation(self, individuals):
        for individual in individuals:
            if random.random() <= MUTATION_PROB:
                geneX = random.randint(0, CHROMOSOME_GENES - 1)
                geneXIndex = GENE_SIZE * geneX
                geneY = random.randint(0, CHROMOSOME_GENES - 1)
                geneYIndex = GENE_SIZE * geneY

                aux = individual[geneXIndex:geneXIndex + GENE_SIZE]
                individual[geneXIndex:geneXIndex + GENE_SIZE] = \
                    individual[geneYIndex:geneYIndex + GENE_SIZE]
                individual[geneYIndex:geneYIndex + GENE_SIZE] = aux
            
        return individuals

    def recombination(self, parents):
            if random.random() <= RECOMBINATION_PROB:
                parent_1 = parents[0]
                parent_2 = parents[1]

                cutPoint = random.randint(0, CHROMOSOME_GENES - 1)
                cutPointIndex = cutPoint * GENE_SIZE
                
                children = []
                children.append(parent_1[:cutPointIndex] + parent_2[cutPointIndex:])
                children.append(parent_2[:cutPointIndex] + parent_1[cutPointIndex:])
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
    print(queens8.best_solution.bin)
    print(queens8.decode_chromosome(queens8.best_solution))
