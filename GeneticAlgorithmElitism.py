# Import necessary libraries
import random
import math
import select
from typing import TypedDict
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

random.seed(42)


# Genetic Algorithm
class Candidate(TypedDict):
    path: list[int]
    dist: int


pass


class GAE:
    def __init__(
        self,
        cities: dict[int, tuple[int, int]],
        populationSize: int = 150,
        crossoverRate: float = 0.75,
        mutationRate: float = 0.05,
        maxMutationStrength: int | None = None,
        numOfGenerations: int = 300,
        elitismRate: float = 0.25,
    ):
        self.cities: dict[int, tuple[int, int]] = cities
        self.populationSize: int = populationSize
        self.crossoverRate: float = crossoverRate
        self.mutationRate: float = mutationRate
        self.maxMutationStrength: int = (
            maxMutationStrength if maxMutationStrength else len(cities) - 1
        )
        self.numOfGenerations: int = numOfGenerations
        self.elitismRate: float = elitismRate
        self.community: list[Candidate] = []
        for i in range(self.populationSize):
            gene = [1] + random.sample(list(range(2, len(cities) + 1)), len(cities) - 1)
            candidate: Candidate = {
                "path": gene,
                "dist": self.calculateTotalDistance(gene),
            }
            self.community.append(candidate)
        pass
        self.community.sort(key=lambda x: x["dist"])
        self.iteration: int = 0
        self.bestDistance: int = self.community[0]["dist"]
        self.bestSolution: list[int] = self.community[0]["path"]
        self.historyDistances: list[int] = [self.bestDistance]
        self.historySolutions: list[list[int]] = [self.bestSolution]

    pass

    def run(self, verbose: bool = False) -> None:
        """執行遺傳演算法（加入 Elitism 的版本）"""
        for self.iteration in range(1, self.numOfGenerations + 1):

            if verbose and self.iteration % 10 == 0:  # 每10代印一次，避免輸出太多
                print(
                    f"Iteration {self.iteration:3d} | Best Distance: {self.community[0]['dist']:8.2f}"
                )
            pass
            newCommunity: list[Candidate] = []

            # ====================== 1. 精英保留 (Elitism) ======================
            elite_count = max(
                2, int(self.populationSize * self.elitismRate)
            )  # 保留約 8% 的最佳個體
            newCommunity.extend(self.community[:elite_count])

            # ====================== 2. 產生新子代 ======================
            num_to_generate = self.populationSize - elite_count

            for _ in range(num_to_generate):
                # 選擇兩個不同的父母
                p1, p2 = self.select_two_parents()

                # 交叉
                if random.random() < self.crossoverRate:
                    newPath = self.crossover(p1["path"], p2["path"])
                else:
                    newPath = p1["path"].copy()

                # 突變
                if random.random() < self.mutationRate:
                    newPath = self.mutation(newPath)

                # 建立新的候選解
                newChild: Candidate = {
                    "path": newPath,
                    "dist": self.calculateTotalDistance(newPath),
                }
                newCommunity.append(newChild)
            pass
            # ====================== 3. 更新族群 ======================
            self.community = newCommunity

            # 排序（距離由小到大）
            self.community.sort(key=lambda x: x["dist"])

            # 更新歷史最佳解
            if self.community[0]["dist"] < self.bestDistance:
                self.bestDistance = self.community[0]["dist"]
                self.bestSolution = self.community[0]["path"].copy()
                self.historyDistances.append(self.bestDistance)
                self.historySolutions.append(self.bestSolution)
            pass

        # ====================== 結束後畫圖 ======================
        if verbose:
            plt.figure(figsize=(10, 5))
            plt.plot(self.historyDistances, "r-", linewidth=2, label="Best Distance")
            plt.xlabel("Iteration")
            plt.ylabel("Distance")
            plt.title("GA Performance on TSP")
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.show()
        pass

    pass

    def get_weights(self) -> list[float]:
        """
        get weights for each member in the community
        based on their distance to the target
        """
        if not self.community:
            return []

        # get all distances from the community
        distances = [c["dist"] for c in self.community]
        min_dist = min(distances)

        weights = []
        for dist in distances:
            if dist == 0:
                weights.append(100.0)
            else:
                # use 1.0 / (dist + smoothing) to avoid numerical instability
                weights.append(1.0 / (dist + min_dist * 0.01))

        return weights

    pass

    def select_parent(self) -> Candidate:
        """select a parent from the community based on weights"""
        weights = self.get_weights()
        selected = random.choices(self.community, weights=weights, k=1)
        return selected[0]

    pass

    def select_two_parents(self) -> tuple[Candidate, Candidate]:
        """select two parents from the community based on weight"""
        parent1 = self.select_parent()
        parent2 = self.select_parent()

        return parent1, parent2

    pass

    def crossover(self, p1: list[int], p2: list[int]) -> list[int]:
        # if same return a copy()
        if p1 == p2:
            return p1.copy()
        # crossover
        n = len(p1)

        start = random.randint(1, (n - 1) - 2)  # possible range [N,P,P,...,P,N,N]
        end = random.randint(start + 2, n - 1)  # possible range [N,...,S,P,...,P]

        segment = p1[start : end + 1]
        child_path: list[int] = [-1] * n
        child_path[start : end + 1] = segment

        # Step 2: take the remaining cities from P2
        remaining = [city for city in p2 if city not in set(segment)]

        # Step 3: fill the remaining cities into child_path
        idx = 0
        for i in range(n):
            if child_path[i] == -1:  # if still empty
                child_path[i] = remaining[idx]
                idx += 1
        return child_path

    pass

    def mutation(self, solution: list[int]) -> list[int]:
        """mutation function"""
        newSolution: list[int] = solution.copy()

        # keep the first city as 1, and mutate the rest
        mutationStrength = random.randint(
            1, self.maxMutationStrength - 1
        )  # mutationStrength: 1~maxMutationStrength
        startIndex = random.randint(1, len(newSolution) - mutationStrength - 1)
        endIndex = startIndex + mutationStrength

        # suffle the segment
        segment = newSolution[startIndex : endIndex + 1]
        newSolution[startIndex : endIndex + 1] = random.sample(segment, len(segment))

        return newSolution

    pass

    def getSolution(self) -> list[int]:
        return self.community[0]["path"]

    pass

    def getDistance(self) -> int:
        return self.community[0]["dist"]

    pass

    def calculateTotalDistance(self, solution: list[int]) -> int:
        def getdist(a: int, b: int) -> int:
            aCoord: tuple[int, int] = self.cities[a]
            bCoord: tuple[int, int] = self.cities[b]
            distBetweenTwoCities: int = (
                (aCoord[0] - bCoord[0]) ** 2 + (aCoord[1] - bCoord[1]) ** 2
            ) ** 0.5
            return distBetweenTwoCities

        pass

        distList: list[int] = [
            getdist(x, y) for x, y in zip(solution, solution[1:] + [solution[0]])
        ]
        dist: int = sum(distList)
        return dist

    pass


pass


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
    ga = GAE(listOfCities, maxMutationStrength=5)
    startTime: datetime = datetime.now()
    ga.run(False)
    runTime: timedelta = datetime.now() - startTime
    finalDistance: int = ga.getDistance()
    finalSolution: list[int] = ga.getSolution()
    print("")
    print(finalDistance)
    print(finalSolution)
    print("")
    print(runTime)
pass
