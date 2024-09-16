# Dylan Stitt
# Rat Gen
# Unit 1 Lab 1

from math import ceil
from random import triangular, uniform, choice, random
from rat import Rat
import time

GOAL = 50000                # Target average weight (grams)
NUM_RATS = 20               # Max adult rats in the lab
INITIAL_MIN_WT = 200        # The smallest rat (grams)
INITIAL_MAX_WT = 600        # The chonkiest rat (grams)
INITIAL_MODE_WT = 300       # The most common weight (grams)
MUTATE_ODDS = 0.01          # Liklihood of a mutation
MUTATE_MIN = 0.5            # Scalar mutation - least beneficial
MUTATE_MAX = 1.2            # Scalar mutation - most beneficial
LITTER_SIZE = 8             # Pups per litter (1 mating pair)
GENERATIONS_PER_YEAR = 10   # How many generations are created each year
GENERATION_LIMIT = 500      # Generational cutoff - stop breeded no matter what

def initial_population():
    """Create the initial set of rats based on constants"""
    rats = [[],[]]
    mother = Rat("F", INITIAL_MIN_WT)
    father = Rat("M", INITIAL_MAX_WT)

    for r in range(NUM_RATS):
        if r < 10:
            sex = "M"
            ind = 0
        else:
            sex = "F"
            ind = 1

        wt = calculate_weight(sex, mother, father)
        R = Rat(sex, wt)
        rats[ind].append(R)
    
    return rats


def calculate_weight(sex, mother, father):
    """Generate the weight of a single rat"""
    
    if mother.getWeight() > father.getWeight():
        min = father.getWeight()
        max = mother.getWeight()
    else:
        max = father.getWeight()
        min = mother.getWeight()    

    if sex == "M":
        wt = int(triangular(min, max, max))
    else:
        wt = int(triangular(min, max, min))

    return wt


def mutate(pups):
    """Check for mutability, modify weight of affected pups"""
    
    for ind in range(len(pups)):
        for pup in pups[ind]:
          odds = random()
          if odds <= MUTATE_ODDS:
            pup.setWeight(ceil(pup.getWeight()*uniform(MUTATE_MIN, MUTATE_MAX))) 
    return pups  


def breed(rats):
    """Create mating pairs, create LITTER_SIZE children per pair"""
    children = [[], []]
    rats[0] = sorted(rats[0], key=lambda x: random())
    rats[1] = sorted(rats[1], key=lambda x: random())
    
    for i in range(10):
        mother = rats[1][i]
        father = rats[0][i]
        mother.litters += 1
        father.litters += 1
        for j in range(LITTER_SIZE):
            sex = choice(['M', 'F'])
            wt = calculate_weight(sex, mother, father)

            if sex == 'M':
                children[0].append(Rat(sex, wt))
            else:
                children[1].append(Rat(sex, wt))

    return children, rats  


def select(allRats, currentLargest):
    '''Choose the largest viable rats for the next round of breeding'''
    rats = [[], []]

    for ind in range(len(allRats)):
        r = sorted(allRats[ind], key=lambda x: x.getWeight())[::-1]
        
        for rat in r:
            if rat.canBreed() and len(rats[ind]) < 10:
                rats[ind].append(rat)

        if r[ind].getWeight() > currentLargest:
            currentLargest = r[ind].getWeight()
    
    return rats, currentLargest


def calculate_mean(rats):
    '''Calculate the mean weight of a population'''
    sumWt1 = [i.getWeight() for i in rats[1]]
    sumWt2 = [i.getWeight() for i in rats[0]]
    sumWt = sum([sum(sumWt1), sum(sumWt2)])
    return sumWt // NUM_RATS


def fitness(rats):
    """Determine if the target average matches the current population's average"""
    mean = calculate_mean(rats)
    return mean >= GOAL, mean


def report(gens, largest, t, avg):
    print('Simulation Results'.center(50, ' '))
    print(f'\nIt took {gens} generations to complete the simulation')
    print(f'\nYears: ~{gens/10} years')
    print(f'\nTime For Simulation to Run: {t} secs')
    print(f'\nThe largest rat ever populated was {largest}g\n')

    print('\nEvery Generation Average:\n')
    count = 0
    for i in avg:
        print(i, end='\t')
        count += 1
        if count == 10:
            count = 0
            print()


def main():
    start = time.time()
    rats = initial_population()
    gens = 0
    largest = 0
    avg = []
    breeding = True

    while gens < GENERATION_LIMIT and breeding:
        gens += 1

        litter, parents = breed(rats)
        litter = mutate(litter)
        
        for i in range(2):
            for p in parents[i]:
                litter[i].append(p)

        rats, largest = select(litter, largest)

        fit = fitness(rats)
        avg.append(fit[1])
        if fit[0]:
            breeding = False

    end = time.time()
    report(gens, largest, round(end-start, 4), avg)

if __name__ == '__main__':
    main()
