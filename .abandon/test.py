import time
import random

from SimulatedAnnealing import SA
from GeneticAlgorithm import GA
from eval import run_multiple_seeds

listOfCities: dict[int, tuple[int, int]] = {
    1: (10, 10),
    2: (20, 30),
    3: (15, 60),
    4: (40, 20),
    5: (50, 40),
    6: (60, 80),
    7: (70, 20),
    8: (80, 60),
    9: (90, 10),
    10: (25, 85),
    11: (45, 70),
    12: (55, 15),
    13: (65, 50),
    14: (30, 40),
    15: (70, 70),
    16: (20, 80),
    17: (85, 20),
    18: (35, 5),
    19: (10, 70),
    20: (60, 30),
}
print(
    run_multiple_seeds(
        GA,
        listOfCities,
        {
          "populationSize": 200, 
          "crossoverRate": 0.6, 
          "mutationRate": 0.03, 
          "maxMutationStrength": 2, 
          "numOfGenerations": 100
        }
    )
)
