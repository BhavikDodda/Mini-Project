import numpy as np

# Cost matrix
cost_matrix = np.array([
    [0, 1, 3, 2, 4],
    [0, 1, 4, 3, 2],
    [1, 2, 4, 0, 3],
    [3, 0, 2, 4, 1],
    [3, 4, 2, 1, 0]
])

n = cost_matrix.shape[0]  # Number of tasks/workers (assumes a square matrix)

# DP table (Initialize all values with infinity)
INF = float('inf')
dp = [INF] * (1 << n)  # There are 2^n states
dp[0] = 0  # Base case: No tasks assigned → cost is 0

# Parent tracking for backtracking multiple solutions
parent = {mask: [] for mask in range(1 << n)}  # Dictionary to store multiple parents

# DP Transition
for mask in range(1 << n):  # Iterate through all possible worker assignments
    i = bin(mask).count('1')  # Number of tasks assigned so far
    if i >= n:  # If all tasks are assigned, skip
        continue

    for j in range(n):  # Try assigning worker j
        if not (mask & (1 << j)):  # If worker j is not assigned
            new_mask = mask | (1 << j)  # Assign worker j
            new_cost = dp[mask] + cost_matrix[i][j]

            if new_cost < dp[new_mask]:  # Found a better cost
                dp[new_mask] = new_cost
                parent[new_mask] = [(mask, j)]  # Replace with new optimal parent

            elif new_cost == dp[new_mask]:  # Another way to achieve the same optimal cost
                parent[new_mask].append((mask, j))  # Store multiple optimal parents

# Optimal cost from DP table
optimal_cost = dp[(1 << n) - 1]  # Full assignment mask (all tasks assigned)

# Function to reconstruct all assignments
def backtrack(mask):
    if mask == 0:
        return [[]]  # Base case: No assignments made yet

    assignments = []
    for prev_mask, j in parent[mask]:  # Explore all valid previous states
        prev_assignments = backtrack(prev_mask)  # Recursively backtrack
        i = bin(prev_mask).count('1')  # Get the task number from previous mask

        for assign in prev_assignments:
            assignments.append(assign + [(i, j)])

    return assignments

# Find all optimal assignments
all_optimal_assignments = backtrack((1 << n) - 1)

# Output results
print("Optimal Cost:", optimal_cost)
print("All Optimal Assignments:")
for assignment in all_optimal_assignments:
    print(assignment)
