import sys, time, numpy, random


#Individual has a value and fitness and knows how to print itself
class Individual:
    EvaluateCount = 0
    BestFitness = 0
    def __init__(self, value):
        if value is None:
            self.value = numpy.array(numpy.random.random_integers(0, 1, VALUE_LENGTH), dtype='bool')
        else:
            self.value = value
        self.fitness = FITNESS(self.value)
        Individual.EvaluateCount += 1
  
    def __str__(self):
        return "".join(str(int(i)) for i in self.value)

    def __repr__(self):
        return "".join(str(int(i)) for i in self.value)

#Uniform crossover
def crossover(a,b):
    g, h = a.value.copy(), b.value.copy()
    split_point = random.randint(0, VALUE_LENGTH - 1)
    g = g.tolist()
    h = h.tolist()
    j = g[:split_point] + h[split_point:]
    k = g[split_point:] + h[:split_point]
    l = numpy.array(j)
    m = numpy.array(k)
    return (Individual(l), Individual(m))

def xover(a, b):
    g, h = a.value.copy(), b.value.copy()
    for pt in range(len(g)):
        if numpy.random.random() < 0.5:
            g[pt], h[pt] = h[pt], g[pt]
    return (Individual(g), Individual(h))

#Per-gene bit-flip mutation
def mutate(a):
    g = a.value.copy()
    for pt in range(len(g)):
        if numpy.random.random() < MUTATE_RATE:
            g[pt] = not g[pt]
            #print("mutate")
    return Individual(g)

def stats(pop, gen):
    best = max(pop, key=lambda x: x.fitness)
    #print ("Generation: %d Average Value: %.2f Best Value: %s Best Fitness: %d" % (gen + 1, numpy.mean([i.fitness for i in pop]), str(best), best.fitness))
    #print ("Generation: %d Best Value: %s Best Fitness: %d" % (gen+1, str(best), best.fitness))
    #if Individual.BestFitness < best.fitness:
    #    Individual.BestFitness = best.fitness
    #return (best.fitness >= SUCCESS_THRESHOLD)
    #return best.fitness
    return numpy.mean([i.fitness for i in pop]), best.fitness

#Use many tournaments to get parents
def tournament (items, n, tsize=2):
    
    for i in range(n):
        candidates = random.sample(items, tsize)
        #print(candidates)
        #print('max(candidates, key=lambda x: x.fitness) = {}'.format(max(candidates, key=lambda x: x.fitness)))
        yield max(candidates, key=lambda x: x.fitness)

def tournament2(items, n, tsize=2):
    newpop = []
    for i in range(n):
        candidates = random.sample(items, tsize)
        newpop.append(max(candidates, key=lambda x: x.fitness))
    return newpop    

#Run one generation
def step(pop):
    newpop = []
    parents = SELECTION(pop, len(pop) + 1) # one extra for final crossover
    
    #crossoverBoolean = True
    #print (len(newpop), len(pop))
    while len(newpop) < len(pop):
    #for i in range(len(pop)):
        #if crossoverBoolean and numpy.random.random() < CROSSOVER_RATE:
        if numpy.random.random() < CROSSOVER_RATE:
            # crossover and mutate to get two new individuals
            newpop.extend(xover(parents.__next__(), parents.__next__()))
            #print (pop)
            #crossoverBoolean = False
            #print ("crossover")
            #print (newpop)
        else:
            # clone and mutate to get two new individual
            
            newpop.append(parents.__next__())
            #newpop.append(parents.__next__())
            #print (pop)
            #newpop.append(pop)
            #pass
            #print(newpop)
    #print(newpop)
    return newpop


def main(generations, population_size):
    generate = 0
    average = 0
    if len(sys.argv) > 1:
        numpy.random.seed(int(sys.argv[1]))
    #print("GENERATIONS {0}, POPULATION_SIZE {1}, VALUE_LENGTH {2}, CROSSOVER_RATE {3}, MUTATE_RATE {4}".format(GENERATIONS, POPULATION_SIZE, VALUE_LENGTH, CROSSOVER_RATE, MUTATE_RATE))
    pop = [Individual(None) for i in range(population_size)]
    #print (pop)
    stats(pop, 0)
    fitnessList = []
    realBestFitness = 0
    for gen in range(1, generations):
    #for gen in range(1, GENERATIONS):
        pop = step(pop)
        average, bestFitness = stats(pop, gen)
        #bestFitness = stats(pop, gen)
        fitnessList.append(bestFitness)
        if (realBestFitness <= bestFitness):
            realBestFitness = bestFitness
        if (bestFitness >= SUCCESS_THRESHOLD):
            #print("Success")
            #sys.exit()
            #break
            pass
        else:
            
            pass
       #     print("Failure")
    a = Individual.EvaluateCount
    #print (Individual.EvaluateCount)    
    Individual.EvaluateCount = 0
    #return realBestFitness
    #return a
    return average
    
#Parameters
GENERATIONS, POPULATION_SIZE, VALUE_LENGTH, CROSSOVER_RATE, MUTATE_RATE = (500, 20, 32, 0.5, 0.01)
FITNESS, SUCCESS_THRESHOLD = (numpy.sum, VALUE_LENGTH)
SELECTION = tournament
