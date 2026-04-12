# Project Requirement for CIS240 (2026 Spring)

**Objective:**

Students are required to implement two different algorithms to solve the Travelling Salesman Problem (TSP), a classic algorithmic problem in the fields of computer science and operations research. This project aims to enhance your understanding of heuristic and optimization techniques in artificial intelligence.

**Algorithms:**

Students may choose two from the following algorithms to solve the TSP:

1. Hill-Climbing

2. Beam Search

3. Genetic Algorithm

4. Simulated Annealing

**Requirements:**

1. **Implementation**:

   * Implement the selected algorithms in the programming language of your choice (Python, Java, or C++).

   * Ensure your code is well-documented and includes comments to explain key steps.

2. **Input**:

   * The algorithms should accept a list of cities and the coordinates of these cities.

   * There are totally 20 cities. Each line represents a city. The first number is city ID, the second and third numbers are x-coordinate and y-coordinate respectively.

        | city ID | x-coordinate | y-coordinate |
        | ------ | ------ | ------ |
        | 1 | 10 | 10 |
        | 2 | 20 | 30 |
        | 3 | 15 | 60 |
        | 4 | 40 | 20 |
        | 5 | 50 | 40 |
        | 6 | 60 | 80 |
        | 7 | 70 | 20 |
        | 8 | 80 | 60 |
        | 9 | 90 | 10 |
        | 10 | 25 | 85 |
        | 11 | 45 | 70 |
        | 12 | 55 | 15 |
        | 13 | 65 | 50 |
        | 14 | 30 | 40 |
        | 15 | 70 | 70 |
        | 16 | 20 | 80 |
        | 17 | 85 | 20 |
        | 18 | 35 | 5 |
        | 19 | 10 | 70 |
        | 20 | 60 | 30 |

   * The distance between any two cities (a, b ) is calculated using Euclidean distance. dista,b=xa-xb2+ya-yb2

3. **Output:**

   * The first line outputs the total distance of your tour.

   * The second line lists the city sequence starting with 1\.

4. **Parameters**:

   * Define and justify the parameters used in your implemented algorithms, such as:

     * **Hill-Climbing**: Starting point, maximum iterations, neighborhood function.

     * **Beam Search**: Beam width, maximum depth.

     * **Genetic Algorithm**: Population size, mutation rate, crossover rate, number of generations.

     * **Simulated Annealing**: Initial temperature, cooling schedule, stopping criteria.

5. **Performance Evaluation**:

   * Compare the performance of the two algorithms using metrics such as:

     * Total distance of the tour found

     * Execution time

     * Quality of the solution (how close it is to the optimal solution)

6. **Analysis**:

   * Discuss the effects of different parameters on the performance of each algorithm.

   * Analyze the strengths and weaknesses of each algorithm based on empirical results.

7. **Report**:

   * Submit a report that includes:

     * Introduction to the TSP and the chosen two algorithms.

     * Description of the implementation process and any challenges faced.

     * Analysis of results and parameter effects.

     * Conclusion summarizing findings and insights from the project.

8. **Marking Rubric:**

   | Criteria | Excellent (4) | Good (3) | Fair (2) | Poor (1) | Unacceptable (0) | Points |
   | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
   | **Algorithm Implementation** | Fully functional code with no bugs and excellent documentation. | Functional code with minor bugs; well-documented. | Code works with major bugs; some documentation. | Incomplete code; poorly documented. | Code does not run or no code submitted; no documentation. | /4 |
   | **Parameter Definition** | Thorough explanation of parameters with strong justification. | Good explanation of parameters with some justification. | Basic parameter explanation with limited justification. | Minimal explanation of parameters; lacks clarity. | No explanation of parameters. | /4 |
   | **Performance Evaluation** | Comprehensive evaluation; clear metrics and insightful comparisons. | Good evaluation; some metrics presented. | Basic evaluation; limited metrics. | Incomplete evaluation with unclear metrics. | No evaluation provided. | /4 |
   | **Analysis and Discussion** | Deep analysis of results with clear insights and conclusions. | Good analysis; some insights are provided. | Basic analysis with limited insights. | Minimal analysis with unclear conclusions. | No analysis provided. | /4 |
   | **Report Quality** | Well-structured report; clear and concise writing with no errors. | Report is structured with minor errors. | Some structure; contains multiple errors. | Poor structure; unclear writing with many errors. | No report or illegible. | /4 |
