# Import necessary libraries
import random
import math
import matplotlib.pyplot as plt
from datetime import datetime

from exceptiongroup import catch

random.seed(42)


# Simulated Annealing Algorithm
class SA:
    def __init__(
        self,
        cities: dict[int, tuple[int, int]],
        initialTemp: int = 10000,
        coolingRate: float = 0.995,
        maxIterations: int = 10000,
        maxNoChangeIterations: int = 2000,
    ):
        self.cities: dict[int, tuple[int, int]] = cities
        self.temp: float = initialTemp
        self.coolingRate: float = coolingRate
        self.maxIterations: int = maxIterations
        self.maxNoChangeIterations: int = maxNoChangeIterations
        self.solution: list[int] = [1] + random.sample(
            list(range(2, len(cities) + 1)), len(cities) - 1
        )
        self.distance: float = self.calculateTotalDistance(self.solution)
        self.bestDistance: float = self.distance
        self.bestSolution: list[int] = self.solution
        self.iteration: int = 1
        self.noChangeIterations: int = 1
        self.historySolutions: list[list[int]] = [self.solution]
        self.historyDistances: list[float] = [self.distance]
        pass

    def run(self, verbose: bool = False) -> None:
        # print initial state
        if verbose:
            print("-" * 50)
            # print iteration
            print(f"Iteration {self.iteration}")
            # print current temperature
            print(f"Current temperature: {self.temp}")
            # print current distance
            print(f"Current distance: {self.distance}")
            # print current solution
            print(f"Current solution: {self.solution}")
            print("-" * 50)
            pass
        # run algorithm
        while self.iteration < self.maxIterations and self.temp > 0 and self.noChangeIterations < self.maxNoChangeIterations:
            # generate new solution
            newSoultion = self.shuffle(self.solution)
            newDistance = self.calculateTotalDistance(newSoultion)
            X = random.random()
            deltaD = newDistance - self.distance
            try:
                y = 1 if deltaD < 0 else 1 / math.exp(min(700,deltaD / self.temp)) # min() for avoid OverflowError: math range error
            except OverflowError:
                print(f"newDistance: {newDistance}, self.distance: {self.distance}, deltaD: {deltaD}, self.temp: {self.temp}")
                quit()
            pass
            # if X < y, accept new solution
            if not(X < y):
                self.noChangeIterations += 1
                continue # reject new solution
            pass
            self.noChangeIterations = 0
            # accept new solution
            self.solution = newSoultion
            self.distance = newDistance
            self.temp = self.temp * self.coolingRate
            self.iteration += 1
            # print verbose
            if verbose:
                print("-" * 50)
                # print iteration
                print(f"Iteration {self.iteration}")
                # print current temperature
                print(f"Current temperature: {self.temp}")
                # print current distance
                print(f"Current distance: {self.distance}")
                # print current solution
                print(f"Current solution: {self.solution}")
                print("-" * 50)
                self.historyDistances.append(self.distance)
                self.historySolutions.append(self.solution)
                pass
            if newDistance < self.bestDistance:
                self.bestDistance = newDistance
                self.bestSolution = newSoultion
                pass
            pass
        if verbose:
            plt.figure(figsize=(10, 5)) 
            plt.plot(list(range(1,len(self.historyDistances)+1)),self.historyDistances, 'r-', linewidth=2, label='Distance')
            plt.xlabel("Iteration")
            plt.ylabel("Distance")
            plt.title("Distance vs Iteration")
            plt.legend()
            plt.tight_layout()
            plt.show()
            pass
        pass

    def shuffle(self, solution: list[int]) -> list[int]:
        newSolution: list[int] = solution.copy()
        # 1 to len(solution) cuz must start with the first city (city 1), so won't shuffle first city
        indices: list[int] = random.sample(range(1, len(solution)), 2)
        newSolution[indices[0]], newSolution[indices[1]] = (
            newSolution[indices[1]],
            newSolution[indices[0]],
        )
        return newSolution

    def getSolution(self) -> list[int]:
        return self.solution

    def getDistance(self) -> float:
        return self.distance

    def getBestSolution(self) -> list[int]:
        return self.bestSolution

    def getBestDistance(self) -> float:
        return self.bestDistance

    def calculateTotalDistance(self, solution: list[int]) -> float:
        def getdist(a: int, b: int) -> float:
            aCoord: tuple[int, int] = self.cities[a]
            bCoord: tuple[int, int] = self.cities[b]
            distBetweenTwoCities: int = (
                (aCoord[0] - bCoord[0]) ** 2 + (aCoord[1] - bCoord[1]) ** 2
            ) ** 0.5
            return distBetweenTwoCities

        distList: list[float] = [
            getdist(x, y) for x, y in zip(solution, solution[1:] + [solution[0]])
        ]
        dist: float = sum(distList)
        return dist


# Start the algorithm
if __name__ == "__main__":
    # Define the cities and their coordinates
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
    # Create a list of City objects
    sa = SA(listOfCities, 10000, 0.995, 10000, 2000)
    startTime = datetime.now()
    sa.run(False)
    runTime = datetime.now() - startTime
    finalDistance = sa.getDistance()
    finalSolution = sa.getSolution()
    bestDistance = sa.getBestDistance()
    bestSolution = sa.getBestSolution()
    print("")
    print(finalDistance)
    print(finalSolution)
    print("")
    print(runTime)
    print(bestDistance)
    print(bestSolution)
    pass
    # end of main function
