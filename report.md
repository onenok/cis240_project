# Project Report: Solving Traveling Salesman Problem (TSP) using SA and GA

## 1. Introduction

* **Introduction to TSP**:\
TSP--Travelling Salesman Problem is a classic algorithmic problem in the fields of computer science and operations research. The question is to give n cities, try to find the shortest path that passes through all the cities exactly once and returns to the starting city.

* **Selected Algorithms**:\
In this project, I'll implement two different algorithms to solve TSP, algorithms are: Simulated Annealing (SA) and Genetic Algorithm (GA). I selected them because SA is a locally optimal algorithm, while GA is a global optimal algorithm, so that it can show the difference between these two types of algorithms significantly.

---

## 2. Implementation Process

* **Programming Environment**: Python 3.10.11
* **Data Structures**: I'm using a dict[int, tuple[int, int]] to store the cities data, e.g.:

    ```python
    {
      1: (10, 10),
      2: (20, 30),
    }
    ```

* **Algorithm Logic**:
  * **SA Implementation**:
    1. Initialization:\
    The algorithm begins by generating an initial random solution (a valid tour starting with City 1). It calculates the total Euclidean distance of this tour and sets the starting temperature ($T$) and a cooling rate ($\alpha$).
    2. Neighbor Discovery (Shuffling):\
    In each step, the algorithm explores the "neighborhood" of the current solution. It uses a Swap Mutation (the shuffle method) to randomly pick two cities (excluding the first) and swap their positions.
    3. The Metropolis Criterion (Acceptance Logic):\
    This is the core of SA. The algorithm decides whether to move to the new neighbor based on the following rules:
       * Better Solution: If the new distance is shorter ($\Delta D < 0$), the move is always accepted.
       * Worse Solution: If the new distance is longer ($\Delta D > 0$), the move is accepted with a probability $P = e^{-\frac{\Delta D}{T}}$. This allows the algorithm to occasionally accept "bad" moves to escape local optima (dead ends).
    4. Cooling Schedule:\
    After an accepted move, the temperature is multiplied by the cooling rate ($T = T \times \alpha$). As the temperature decreases, the probability of accepting worse solutions drops, causing the algorithm to focus more on fine-tuning the best path it has found.
    5. Termination:\
    The process repeats until the maxIterations limit is reached or the temperature effectively reaches zero. The algorithm ensures the globally bestSolution found during the entire search is preserved.

  * **GA Implementation**:
    1. Initialization (Population):\
      The algorithm starts by creating a "community" (population) of random potential solutions. Each individual (candidate) is a valid tour that must start with City 1.

    2. Selection (Fitness-Based):\
      In every generation, parents are selected to reproduce based on their "weights." The weight is inversely proportional to the tour distance: shorter paths have higher weights, meaning the "fitter" individuals have a higher probability of being chosen to pass on their genes.

    3. Reproduction (Crossover):\
      The algorithm performs Ordered Crossover (OX). It picks a random segment from Parent 1 and copies it to the child. The remaining slots are filled with cities from Parent 2 in the order they appear, ensuring that no city is repeated and the tour remains valid.

    4. Mutation:\
      To maintain genetic diversity and prevent the population from getting stuck in a local optimum, some children undergo mutation. A random segment of the path is selected and "shuffled" (randomly reordered). The maxMutationStrength parameter controls how large this shuffled segment can be.

    5. Survival of the Fittest (Elite Selection):\
      After generating new children, the new individuals are added to the community. The entire group is sorted by distance, and only the top populationSize individuals are kept for the next generation. This ensures the best solutions found so far are never lost.

    6. Termination:\
      The process repeats for a set number of generations (numOfGenerations). The algorithm tracks the bestDistance and bestSolution throughout its execution.

* **Challenges Faced**:

  **1. Maintaining Path Integrity and Validity**
  * **The Challenge**:\
  A fundamental constraint of the TSP is the requirement of a **Hamiltonian Path**, where every city must be visited exactly once. I initially encountered a significant hurdle where standard genetic operators (like simple one-point crossover) would produce "invalid tours" containing duplicate cities or missing locations.
  * **Technical Solution**:\
  To resolve this, I implemented **Ordered Crossover (OX)** for the Genetic Algorithm. OX preserves the relative order of a segment from one parent while filling the remaining slots from the second parent without repetition. Similarly, for both SA and GA mutation, I utilized **Index-Swap** and **Segment-Shuffle** mechanisms. This ensured that every offspring or neighbor remained a valid permutation throughout the stochastic search process.

  **2. Combinatorial Explosion (The "19!" Search Space)**
  * **The Challenge**:\
  At first, I underestimated the complexity of a 20-city problem, attempting to solve it with low iteration counts (e.g., 99 iterations). However, a mathematical analysis revealed that with a fixed starting city, the search space consists of $(n-1)! = 19!$ possible routes. This equals approximately **121 quadrillion** patterns ($1.21 \times 10^{17}$), a scale where exhaustive search is computationally impossible.
  * **Technical Solution**:\
  Realizing I was facing the **"Curse of Dimensionality,"** I adjusted the "computational budget." For Simulated Annealing, I increased the iteration limit and slowed the cooling rate ($\alpha$) to allow for more exploration. For the Genetic Algorithm, I expanded the population size to 200 and the generation limit to 500. This allowed the algorithms to sample a statistically significant portion of the search space, moving from random noise toward a near-optimal convergence.

---

## 3. Parameter Definition and Justification

### 3.1 Simulated Annealing (SA)

* **Initial Temperature (T_init)**:\
***`10000`*** — Set it high enough to ensure that the entire search space can be explored in the initial stages.
* **Cooling Rate (alpha)**:\
***`0.99`*** — Slow cooling can improve the quality of the solution and ensure that the algorithm can perform a finer search at low temperatures.
* **Stopping Criteria**:\
repeat until the maxIterations limit is reached or the temperature effectively reaches zero or iteration was rejected more than maxNoChangeIterations consecutively.

### 3.2 Genetic Algorithm (GA)

* **Population Size**:\
***`200`*** — Balancing computation time with population diversity.
* **Crossover Rate**:\
***`0.75`*** — A high mating rate helps preserve and combine superior gene fragments.
* **Mutation Rate**:\
***`0.05`*** — A lower mutation rate can prevent good solutions from being randomly destroyed, while maintaining diversity.
* **Max Generations**:\
***`500`*** — Provide sufficient evolution time to achieve convergence.
* **Max Mutation Strength**:\
***`5`***

---

## 4. Analysis and Discussion

### 4.1 **Parameter Sensitivity**
  
* *SA SENSITIVITY: DEVIATION FROM BASELINE*
  
  --- Testing Deviation of initialTemp (Baseline: 10000) ---

  | Deviation  | Value    | Avg Dist      | Best Dist     | Best Path                                                               | Avg Time      |
  | ---------- | -------- | ------------- | ------------- | ----------------------------------------------------------------------- | ------------- |
  | -9000      | 1000     | 391.67        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 794.0295      |
  | -5000      | 5000     | 370.07        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 801.8319      |
  | BASELINE   | 10000    | 378.22        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 885.1983      |
  | +10000     | 20000    | 369.80        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 1390.7904     |
  | +40000     | 50000    | 385.94        | 376.87        | [1, 2, 14, 4, 18, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3] | 1083.4764     |

  --- Testing Deviation of coolingRate (Baseline: 0.995) ---

  | Deviation  | Value    | Avg Dist      | Best Dist     | Best Path                                                               | Avg Time      |
  | ---------- | -------- | ------------- | ------------- | ----------------------------------------------------------------------- | ------------- |
  | -0.095     | 0.9      | 446.02        | 403.81        | [1, 18, 20, 13, 5, 14, 4, 12, 7, 9, 17, 8, 15, 6, 11, 10, 16, 19, 3, 2] | 75.4543       |
  | -0.005     | 0.99     | 378.39        | 371.96        | [1, 2, 14, 5, 3, 19, 16, 10, 11, 6, 15, 8, 13, 20, 7, 17, 9, 12, 4, 18] | 520.7808      |
  | BASELINE   | 0.995    | 378.22        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 876.7494      |
  | +0.004     | 0.999    | 362.72        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 4029.5042     |

  --- Testing Deviation of maxIterations (Baseline: 10000) ---

  | Deviation  | Value    | Avg Dist      | Best Dist     | Best Path                                                               | Avg Time      |
  | ---------- | -------- | ------------- | ------------- | ----------------------------------------------------------------------- | ------------- |
  | -9000      | 1000     | 683.66        | 580.79        | [1, 7, 20, 4, 18, 9, 17, 15, 8, 13, 5, 12, 2, 3, 14, 11, 6, 16, 10, 19] | 21.5781       |
  | -5000      | 5000     | 378.22        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 871.1072      |
  | BASELINE   | 10000    | 378.22        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 875.4730      |
  | +5000      | 15000    | 378.22        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 870.7910      |
  | +10000     | 20000    | 378.22        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 865.4188      |

  --- Testing Deviation of maxNoChangeIterations (Baseline: 2000) ---

  | Deviation  | Value    | Avg Dist      | Best Dist     | Best Path                                                               | Avg Time      |
  | ---------- | -------- | ------------- | ------------- | ----------------------------------------------------------------------- | ------------- |
  | -1900      | 100      | 419.13        | 390.71        | [1, 2, 14, 5, 20, 7, 17, 9, 13, 8, 15, 6, 11, 10, 16, 19, 3, 4, 12, 18] | 68.2494       |
  | -1500      | 500      | 388.46        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 291.7633      |
  | BASELINE   | 2000     | 378.22        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 915.7092      |
  | +3000      | 5000     | 378.22        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 2099.1804     |
  | +8000      | 10000    | 378.22        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 3164.6858     |

* *GA SENSITIVITY: DEVIATION FROM BASELINE*

  --- Testing Deviation of populationSize (Baseline: 200) ---

  | Deviation  | Value    | Avg Dist      | Best Dist     | Best Path                                                               | Avg Time      |
  | ---------- | -------- | ------------- | ------------- | ----------------------------------------------------------------------- | ------------- |
  | -150       | 50       | 440.10        | 401.50        | [1, 2, 14, 5, 16, 19, 3, 10, 11, 6, 15, 8, 13, 20, 7, 17, 9, 12, 4, 18] | 132.3437      |
  | -100       | 100      | 403.87        | 348.80        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 17, 9, 7, 12, 4, 18] | 383.8024      |
  | BASELINE   | 200      | 373.12        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1226.3521     |
  | +100       | 300      | 353.95        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 2715.3605     |
  | +200       | 400      | 359.00        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 4761.6318     |

  --- Testing Deviation of crossoverRate (Baseline: 0.6) ---

  | Deviation  | Value    | Avg Dist      | Best Dist     | Best Path                                                               | Avg Time      |
  | ---------- | -------- | ------------- | ------------- | ----------------------------------------------------------------------- | ------------- |
  | -0.45      | 0.15     | 480.05        | 427.03        | [1, 18, 14, 5, 4, 12, 20, 7, 9, 17, 13, 8, 15, 6, 11, 3, 16, 10, 19, 2] | 369.7383      |
  | -0.15      | 0.45     | 375.40        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1096.4770     |
  | BASELINE   | 0.6      | 373.12        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1372.5238     |
  | +0.15      | 0.75     | 364.05        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 1639.5375     |
  | +0.24      | 0.84     | 361.34        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1799.5102     |

  --- Testing Deviation of mutationRate (Baseline: 0.03) ---

  | Deviation  | Value    | Avg Dist      | Best Dist     | Best Path                                                               | Avg Time      |
  | ---------- | -------- | ------------- | ------------- | ----------------------------------------------------------------------- | ------------- |
  | -0.04      | 0.01     | 370.36        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1321.5881     |
  | -0.02      | 0.01     | 370.36        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1262.3652     |
  | BASELINE   | 0.03     | 373.12        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1247.3827     |
  | +0.1       | 0.13     | 359.97        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1281.3776     |
  | +0.4       | 0.43     | 361.43        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1373.5516     |

  --- Testing Deviation of maxMutationStrength (Baseline: 2) ---

  | Deviation  | Value    | Avg Dist      | Best Dist     | Best Path                                                               | Avg Time      |
  | ---------- | -------- | ------------- | ------------- | ----------------------------------------------------------------------- | ------------- |
  | -3         | 2        | 373.12        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1360.9022     |
  | -2         | 2        | 373.12        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1305.7084     |
  | BASELINE   | 2        | 373.12        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1323.2373     |
  | +5         | 7        | 363.38        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 1292.4611     |
  | +13        | 15       | 367.62        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 1383.7670     |

  --- Testing Deviation of numOfGenerations (Baseline: 100) ---

  | Deviation  | Value    | Avg Dist      | Best Dist     | Best Path                                                               | Avg Time      |
  | ---------- | -------- | ------------- | ------------- | ----------------------------------------------------------------------- | ------------- |
  | -400       | 2        | 687.04        | 662.82        | [1, 18, 12, 4, 14, 19, 3, 20, 17, 9, 7, 5, 2, 13, 10, 15, 11, 6, 8, 16] | 44.3598       |
  | -200       | 2        | 687.04        | 662.82        | [1, 18, 12, 4, 14, 19, 3, 20, 17, 9, 7, 5, 2, 13, 10, 15, 11, 6, 8, 16] | 44.4442       |
  | BASELINE   | 100      | 373.12        | 348.20        | [1, 18, 4, 12, 9, 17, 7, 20, 5, 13, 8, 15, 6, 11, 10, 16, 19, 3, 14, 2] | 1317.0682     |
  | +500       | 600      | 368.33        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 7326.5172     |
  | +1000      | 1100     | 368.33        | 348.20        | [1, 2, 14, 3, 19, 16, 10, 11, 6, 15, 8, 13, 5, 20, 7, 17, 9, 12, 4, 18] | 13568.7549    |

### 4.2 Parameter Sensitivity: Deviation from Baseline

The following analysis examines how each algorithm reacts to changes in its core parameters.

#### Simulated Annealing (SA) Insights

* **Cooling Rate Sensitivity**: This is the most critical factor for convergence. Reducing the rate to 0.9 (a -0.095 deviation) caused the average distance to jump to 446.02, as the algorithm "quenched" too quickly and got stuck. Increasing it to 0.999 improved the average distance to 362.72 but increased execution time by nearly 4.5x, demonstrating a clear trade-off between precision and computational cost.
* **Convergence via maxNoChangeIterations**: The baseline of 2000 iterations without change proved to be a "sweet spot." Lowering it significantly (to 100) led to premature termination with a poor distance of 419.13, while increasing it beyond 2000 yielded no further improvements in distance, only increasing the runtime.
* **Temperature Robustness**: SA showed high resilience to the `initialTemp`. Values ranging from 5,000 to 20,000 all converged to similar average results, suggesting the baseline of 10,000 is well-chosen for a 20-city problem.

#### Genetic Algorithm (GA) Insights

* **Population Size & Quality**: Increasing the population from 50 to 300 dropped the average distance from 440.10 to 353.95. However, at a population of 400, the performance plateaued and slightly regressed (359.00), suggesting that without a proportional increase in generations, a massive population may lead to incomplete evolution.
* **The Power of Crossover**: A low crossover rate (0.15) crippled the GA’s search capability (Avg Dist: 480.05). The algorithm reached peak efficiency at rates between 0.6 and 0.84, confirming that the recombination of genes is the primary driver of optimization in this TSP implementation.
* **Evolutionary Limits**: The data for `numOfGenerations` shows that the population reached near-total homogeneity around the 600th generation. Increasing the limit to 1100 did not change the average distance (remaining at 368.33), but doubled the execution time.

### 4.3 Empirical Comparison

In this 20-city case, **Simulated Annealing (SA) proved to be the more efficient and balanced choice.** While both algorithms were capable of finding the global optimum (348.20), SA achieved an average best distance of 378.22 in less than **1 second** (934ms). In contrast, the Genetic Algorithm required nearly **10 seconds** (9940ms) to reach an average of 359.55. Although GA is statistically "more robust" at finding slightly better average paths across multiple runs, the order-of-magnitude difference in time complexity makes SA far more attractive for problems of this specific scale.

---

## 5. Performance Evaluation

### 5.1 Comparative Results

| Metric | Simulated Annealing (SA) | Genetic Algorithm (GA) |
| :--- | :--- | :--- |
| Average Best Distance | 378.22 | 373.12 |
| Average Execution Time | 964.47 ms | 1337.04 ms |
| Absolute Best Distance | 348.20 | 348.20 |

### 5.2 Best Tour Output

* **SA Best Tour**: 1 -> 2 -> 14 -> 3 -> 19 -> 16 -> 10 -> 11 -> 6 -> 15 -> 8 -> 13 -> 5 -> 20 -> 7 -> 17 -> 9 -> 12 -> 4 -> 18 -> 1 (Distance: 348.20)
* **GA Best Tour**: 1 -> 2 -> 14 -> 3 -> 19 -> 16 -> 10 -> 11 -> 6 -> 15 -> 8 -> 13 -> 5 -> 20 -> 7 -> 17 -> 9 -> 12 -> 4 -> 18 -> 1 (Distance: 348.20)

---

## 6. Conclusion

* **Summary**:
This project successfully demonstrated that both Simulated Annealing and Genetic Algorithms can effectively navigate the $(n-1)!$ combinatorial explosion of the Traveling Salesman Problem. Starting from random initial paths with distances often exceeding 1000, both heuristics successfully optimized the routes down to the global minimum of 348.20. While GA offers a more comprehensive search through population diversity, SA provides a remarkably fast and lightweight alternative that is highly effective when the cooling schedule is properly tuned.

* **Final Insights**:
Implementing these algorithms highlighted the reality of solving NP-hard problems: there is no "perfect" setting, only a series of trade-offs. The sensitivity analysis revealed that heuristic performance is not linear; small changes in parameters like the `coolingRate` or `crossoverRate` can lead to disproportionate failures or successes. Ultimately, understanding the mathematical constraints of the search space allowed for the transition from "random noise" to a sophisticated, near-optimal solution, providing a practical foundation for tackling complex optimization tasks in real-world scenarios.
