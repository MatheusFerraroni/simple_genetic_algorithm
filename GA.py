import numpy as np


class element:

    def __init__(self, idd, geracao, genome):
        self.idd = idd
        self.geracao = geracao
        self.genome = genome
        self.score = None


    def __repr__(self):
        return "(id="+str(self.idd)+",geracao="+str(self.geracao)+",score="+str(self.score)+")"

class GeneticAlgorithm:

    def __init__(self):
        self.population = []
        self.historic = []
        self.mutation_rate = 0
        self.population_size = 100
        self.iteration_limit = float('inf')
        self.elements_created = 0
        self.best_element_total = None
        self.max_possible_score = float('inf')
        self.create_initial_population()


    def run(self):

        iteration_counter = 0

        while iteration_counter<self.iteration_limit:
            # print(iteration_counter, self.best_element_total)
            self.calculate_score()

            self.population.sort(key=lambda x: x.score, reverse=True) # ordena por score


            score_geracao_medio = 0
            score_geracao_max = float('-inf')
            score_geracao_min = float('inf')
            for i in range(len(self.population)):
                score_geracao_medio += self.population[i].score
                score_geracao_min = min(score_geracao_min, self.population[i].score)
                score_geracao_max = max(score_geracao_max, self.population[i].score)
            score_geracao_medio /= len(self.population)

            # print(score_geracao_min,score_geracao_medio,score_geracao_max)

            # self.population = self.population[0:len(self.population)//2] # descarta pior metade



            if self.best_element_total==None or self.population[0].score > self.best_element_total.score: # salva melhor elemento
                self.best_element_total = self.population[0]


            self.historic.append({"geracao":iteration_counter,"max":score_geracao_max,"min":score_geracao_min,"avg":score_geracao_medio,"best":self.best_element_total.score})



            probs = [0]*len(self.population) # gera array de probs para selecionar parents
            for i in range(len(probs)):
                probs[i] = self.population[i].score
            div = sum(probs)

            if div!=0:
                for i in range(len(probs)):
                    probs[i] /= div
            else:
                probs = [1/len(probs)]*len(probs)


            newPop = []

            while len(newPop)<self.population_size:
                parents = np.random.choice(self.population,size=2,p=probs) #seleciona parents

                new_element = element(self.elements_created, iteration_counter, self.crossover(parents[0].genome, parents[1].genome))

                new_element.genome = self.mutate(new_element.genome)
                newPop.append(new_element)
                self.elements_created += 1

            self.population = newPop

            iteration_counter +=1

            if self.best_element_total.score >= self.max_possible_score:
                break

        return self.best_element_total



    def set_max_score(self, e):
        self.max_possible_score = e

    def set_iteration_limit(self, e):
        self.iteration_limit = e

    def create_initial_population(self):
        for _ in range(self.population_size):
            self.population.append(element(self.elements_created, 0, np.random.randint(low=0,high=8,size=16,dtype=int)))
            self.elements_created += 1

    def set_population_size(self, e):
        self.population_size = e

    def set_mutation_rate(self, e):
        self.mutation_rate = e

    def set_evaluate(self, e):
        self.evaluate = e

    def evaluate(self):
        raise Exception("Should be override")

    def crossover(self, genA, genB):
        c1 = c2 = np.random.randint(low=0,high=len(genA))
        while c2==c1:
            c2 = np.random.randint(low=0,high=len(genA))

        if c1>c2:
            c1, c2 = c2,c1

        new = np.append(np.append(genA[0:c1],genB[c1:c2]),genA[c2:])

        return new

    def calculate_score(self):
        for e in self.population:
            e.score = self.evaluate(e.genome)

    def mutate(self,gen):
        if self.mutation_rate==0:
            return gen
        mutations = 0
        while mutations==0:
            for i in range(len(gen)):
                if np.random.random()<self.mutation_rate:
                    gen[i] = np.random.randint(low=0,high=8)
                    mutations += 1
        return gen