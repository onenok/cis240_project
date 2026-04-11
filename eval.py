import time
import random
from GeneticAlgorithm import GA 
from SimulatedAnnealing import SA 
# helper function to run algorithm multiple times with different seeds
def run_multiple_seeds(algo_class, cities, params, seeds=[42, 43, 44, 45, 46]):
    total_dist = 0.0
    total_time = 0.0
    best_dist_overall = float('inf')
    best_path_overall = []

    for s in seeds:
        # set random seed for this run
        random.seed(s)
        
        # start timer
        start_time = time.perf_counter()
        
        # create and run algorithm instance
        instance = algo_class(cities, **params)
        instance.run(verbose=False)
        
        # stop timer
        run_time = (time.perf_counter() - start_time) * 1000
        
        # get results
        current_dist = instance.getBestDistance()
        current_path = instance.getBestSolution()
        
        # add to totals for average calculation
        total_dist += current_dist
        total_time += run_time
        
        # save the very best path among all seeds
        if current_dist < best_dist_overall:
            best_dist_overall = current_dist
            best_path_overall = current_path

    # calculate averages
    avg_dist = total_dist / len(seeds)
    avg_time = total_time / len(seeds)
    
    return avg_dist, avg_time, best_dist_overall, best_path_overall


def evaluate_comparative_results(cities):
    print("\n" + "="*50)
    print(" COMPARATIVE RESULTS (Average of 5 Seeds)")
    print("="*50)
    
    # baseline parameters for SA
    sa_params = {
        "initialTemp": 10000, 
        "coolingRate": 0.995, 
        "maxIterations": 10000,
        "maxNoChangeIterations": 2000
    }
    
    # baseline parameters for GA
    ga_params = {
        "populationSize": 200, 
        "crossoverRate": 0.6, 
        "mutationRate": 0.03, 
        "maxMutationStrength": 2, 
        "numOfGenerations": 100
    }

    # test SA
    sa_avg_dist, sa_avg_time, sa_best_dist, sa_best_path = run_multiple_seeds(SA, cities, sa_params)
    
    # test GA
    ga_avg_dist, ga_avg_time, ga_best_dist, ga_best_path = run_multiple_seeds(GA, cities, ga_params)

    # print markdown table
    print("\n### Comparative Results\n")
    print("| Metric | Simulated Annealing (SA) | Genetic Algorithm (GA) |")
    print("| :--- | :--- | :--- |")
    print(f"| Average Best Distance | {sa_avg_dist:.2f} | {ga_avg_dist:.2f} |")
    print(f"| Average Execution Time | {sa_avg_time:.2f} ms | {ga_avg_time:.2f} ms |")
    print(f"| Absolute Best Distance | {sa_best_dist:.2f} | {ga_best_dist:.2f} |")
    
    # print best tours
    print("\n### Best Tour Output\n")
    sa_path_str = ' -> '.join(map(str, sa_best_path + [1]))
    ga_path_str = ' -> '.join(map(str, ga_best_path + [1]))
    print(f"* **SA Best Tour**: {sa_path_str} (Distance: {sa_best_dist:.2f})")
    print(f"* **GA Best Tour**: {ga_path_str} (Distance: {ga_best_dist:.2f})")


def evaluate_sa_sensitivity(cities):
    print("* *SA SENSITIVITY: DEVIATION FROM BASELINE*")
    print("")
    
    # baseline settings
    base = {"initialTemp": 10000, "coolingRate": 0.995, "maxIterations": 10000, "maxNoChangeIterations": 2000}
    
    # format: (parameter_name, list_of_offsets)
    tests = [
        ("initialTemp", [-9000, -5000, 0, 10000, 40000]),
        ("coolingRate", [-0.095, -0.005, 0, 0.004]), # results in 0.9, 0.99, 0.995, 0.999
        ("maxIterations", [-9000, -5000, 0, 5000, 10000]),
        ("maxNoChangeIterations", [-1900, -1500, 0, 3000, 8000])
    ]

    for param, offsets in tests:
        print(f"\n--- Testing Deviation of {param} (Baseline: {base[param]}) ---")
        print("")
        print(f"| {'Deviation':^10} | {'Value':<8} | {'Avg Dist':<13} | {'Best Dist':<13} | {'Best Path':<71} | {'Avg Time':<13} |")
        print(f"| {'-'*10} | {'-'*8} | {'-'*13} | {'-'*13} | {'-'*71} | {'-'*13} |")
        for offset in offsets:
            p = base.copy()
            p[param] += offset
            # ensure values stay within logical bounds (especially for rates)
            if param == "coolingRate":
                p[param] = max(0.0001, min(0.9999, p[param]))

            status = "BASELINE" if offset == 0 else f"{offset:+}"
            print(f"| {status:<10} | {p[param]:<8} | {'evaluating...':<13} | {'evaluating...':<13} | {'evaluating...':<71} | {'evaluating...':<13} |", end="\r")
            avg_dist, avg_time, best_dist, best_path = run_multiple_seeds(SA, cities, p)
            print(f"| {status:<10} | {p[param]:<8} | {avg_dist:<13.2f} | {best_dist:<13.2f} | {best_path} | {avg_time:<13.4f} |")

def evaluate_ga_sensitivity(cities):
    print("* *GA SENSITIVITY: DEVIATION FROM BASELINE*")
    print("")
    
    # baseline settings
    base = {"populationSize": 200, "crossoverRate": 0.6, "mutationRate": 0.03, "maxMutationStrength": 2, "numOfGenerations": 100}

    # format: (parameter_name, list_of_offsets)
    tests = [
        ("populationSize", [-150, -100, 0, 100, 200]),
        ("crossoverRate", [-0.45, -0.15, 0, 0.15, 0.24]), # results in 0.3 to 0.99
        ("mutationRate", [-0.04, -0.02, 0, 0.1, 0.4]),    # results in 0.01 to 0.45
        ("maxMutationStrength", [-3, -2, 0, 5, 13]),
        ("numOfGenerations", [-400, -200, 0, 500, 1000])
    ]

    for param, offsets in tests:
        print(f"\n--- Testing Deviation of {param} (Baseline: {base[param]}) ---")
        print("")
        print(f"| {'Deviation':^10} | {'Value':<8} | {'Avg Dist':<13} | {'Best Dist':<13} | {'Best Path':<71} | {'Avg Time':<13} |")
        print(f"| {'-'*10} | {'-'*8} | {'-'*13} | {'-'*13} | {'-'*71} | {'-'*13} |")
        for offset in offsets:
            p = base.copy()
            # use round to avoid floating point precision issues (e.g. 0.0500000000001)
            p[param] = round(p[param] + offset, 4)
            
            # ensure values stay within logical bounds
            if "Rate" in param:
                p[param] = max(0.01, min(0.99, p[param]))
            if "Size" in param or "Generations" in param or "Strength" in param:
                p[param] = max(2, int(p[param]))

            status = "BASELINE" if offset == 0 else f"{offset:+}"
            print(f"| {status:<10} | {p[param]:<8} | {'evaluating...':<13} | {'evaluating...':<13} | {'evaluating...':<71} | {'evaluating...':<13} |", end="\r")
            avg_dist, avg_time, best_dist, best_path = run_multiple_seeds(GA, cities, p)
            print(f"| {status:<10} | {p[param]:<8} | {avg_dist:<13.2f} | {best_dist:<13.2f} | {best_path} | {avg_time:<13.4f} |")


if __name__ == "__main__":
    # Assuming listOfCities is defined here
    # listOfCities = { ... }
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

    print("Starting automated tests with 5 random seeds (42-46)...")
    
    # run comparative evaluation
    evaluate_comparative_results(listOfCities)
    
    # run sensitivity evaluation for SA
    evaluate_sa_sensitivity(listOfCities)
    
    # run sensitivity evaluation for GA
    evaluate_ga_sensitivity(listOfCities)
    
    print("\nAll tests completed!")