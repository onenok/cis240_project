import itertools

def calculateTotalDistance(solution: list[int]) -> int:
    def getdist(a: int, b: int) -> int:
        aCoord: tuple[int, int] = listOfCities[a]
        bCoord: tuple[int, int] = listOfCities[b]
        distBetweenTwoCities: int = (
            (aCoord[0] - bCoord[0]) ** 2 + (aCoord[1] - bCoord[1]) ** 2
        ) ** 0.5
        return distBetweenTwoCities

    distList: list[int] = [
        getdist(x, y) for x, y in zip(solution, solution[1:] + [solution[0]])
    ]
    dist: int = sum(distList)
    return dist


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

# generate all possible permutations of cities

permutations = itertools.permutations(list(range(2, len(listOfCities) + 1)), len(listOfCities) - 1)

# find the shortest path
shortestDist = float('inf')
shortestPath = None
for path in permutations:
    path = list((1,) + path)
    dist = calculateTotalDistance(path)
    if dist < shortestDist:
        shortestDist = dist
        shortestPath = path
print("Shortest path:", shortestPath)
print("Shortest distance:", shortestDist)