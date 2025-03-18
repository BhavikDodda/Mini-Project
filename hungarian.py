import numpy as np
import networkx as nx
from scipy.optimize import linear_sum_assignment

# Cost matrix
cost_matrix = np.array([
    [0, 1],
    [1, 0],
    
])

num_tasks, num_workers = cost_matrix.shape  # Should be square for bipartite matching

# Step 1: Solve using SciPy (Hungarian Algorithm)
row_ind, col_ind = linear_sum_assignment(cost_matrix)
optimal_cost = cost_matrix[row_ind, col_ind].sum()

# Step 2: Create a bipartite graph
B = nx.Graph()

tasks = range(num_tasks)                      # Task nodes: 0 to num_tasks-1
workers = range(num_tasks, num_tasks + num_workers)  # Worker nodes: num_tasks to num_tasks + num_workers - 1

# Add weighted edges between tasks and workers
for i in tasks:
    for j in range(num_workers):
        B.add_edge(i, num_tasks + j, weight=cost_matrix[i, j])

# Step 3: Find the minimum-weight perfect matching
matching = nx.algorithms.matching.min_weight_matching(B, weight="weight")

# Step 4: Compute total cost of this matching
valid_matching = [(i, j) for i, j in matching if i in tasks and j in workers]
matching_cost = sum(cost_matrix[i, j - num_tasks] for i, j in valid_matching)

# Step 5: Check for multiple solutions
has_multiple_solutions = (matching_cost == optimal_cost) and (len(valid_matching) > 1)

# Output results
print("Optimal Cost:", optimal_cost)
print("Initial SciPy Assignment:", list(zip(row_ind, col_ind)))
print("NetworkX Matching:", valid_matching)
print("Are there multiple solutions?", has_multiple_solutions)
