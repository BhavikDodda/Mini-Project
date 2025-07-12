import gurobipy as gp
from gurobipy import GRB

# Example data: rank_matrix[i][j] = rank of room j for person i
rank_matrix = [
    [1, 2, 3],
    [1, 3, 2],
    [1, 2, 3]
]
n = len(rank_matrix)
model = gp.Model("RoomAllocation")
# Variables
x = {}
for i in range(n):
    for j in range(n):
        x[i,j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
# Assignment constraints
for i in range(n):
    model.addConstr(gp.quicksum(x[i,j] for j in range(n)) == 1)
for j in range(n):
    model.addConstr(gp.quicksum(x[i,j] for i in range(n)) == 1)
# Auxiliary variables for ranks
R = [model.addVar(lb=1, ub=n, name=f"R_{i}") for i in range(n)]
for i in range(n):
    model.addConstr(R[i] == gp.quicksum(rank_matrix[i][j]*x[i,j] for j in range(n)))
# Variance = (sum R_i^2)/n - (sum R_i)^2 / n^2
sum_R = gp.quicksum(R[i] for i in range(n))
sum_R_sq = gp.quicksum(R[i]*R[i] for i in range(n))
variance = (sum_R_sq/n)-(sum_R*sum_R)/(n*n)
model.setObjective(variance, GRB.MINIMIZE)
model.optimize()
# Print solution
for i in range(n):
    for j in range(n):
        if x[i,j].X > 0.5:
            print(f"Person {i} → Room {j} (Rank = {rank_matrix[i][j]})")
print(f"Variance = {model.ObjVal}")