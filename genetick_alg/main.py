import random 

class EvoController(object):
    def __init__(self,population_size,iterations,genom_size,fitness_function,crossbreeding=True,mutation_rate=0.01):
        self.mutation_rate = mutation_rate
        self.crossbreeding = crossbreeding
        self.population_size = population_size
        self.genom_size = genom_size
        self.iterations = iterations
        self.fitness_function = fitness_function
        self.current_iteration = 0



    def create_population(population=None):
        if population is None:
            self.population = [random.randint(0,1) for _ in range(self.genom_size)]
        else:
            self.population = population


    def start_evolution(self,steps=None):
        if steps is None:
            while self.current_iteration < self.iterations:
                self.current_iteration += 1
                self.make_iteration()
        else:
            k = 0
            while self.current_iteration < self.iterations and k < steps:
                k += 1
                self.current_iteration += 1
                self.make_iteration()


    def make_iteration(self):
        score_list = []
        for i in self.population:
            score = self.fitness_function(i)
            score_list.append((i,score))
        score_list = random.shuffle(score_list)#                                              FIX IT (most permutations of a long sequence can never be generated)

        self.population = []

        for i in range(n//2):
            being1 = score_list[i*2]
            being2 = score_list[i*2+1]
            if being1[1] > being2[1]:
                self.population.append(being1[0])
            elif being1[1] > being2[1]:
                self.population.append(choice((being1[0],being2[0])))
            else:
                self.population.append(being2[0])

        if self.crossbreeding:
            new = crossbreed(being1[0],being2[0])
        else:
            new = choice((being1[0],being2[0]))

        self.population.append(mutate(new,self.mutation_rate))




def crossbreed(being1,being2):
    return being1[:len(being1)//2] + being2[len(being1)//2:]

def mutate(being,mutation_rate):
    if random.uniform(0,1)<=mutation_rate:
        index = randint(0,len(being))
        being[index] = (being[index] + 1) % 2
    return being

