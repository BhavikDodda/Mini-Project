import random
import itertools

# Parameters
N = 5  # Number of people and rooms
k = 3  # Number of preferences considered

rooms = list(range(N))
people = list(range(N))

# Fixed preference lists (only considering the top-k preferences)
prefList = [
    (0, [0, 1, 3]),
    (1, [2, 0, 3]),
    (2, [2, 1, 0]),
    (3, [1, 3, 2]),
    (4, [1, 0, 3])
]
print("Person, Top-k Allotment Preferences")
print(prefList)

# Random initial allotment (room -> person)
print("\n(rooms, people)")
random.shuffle(people)
allot = {rooms[i]: people[i] for i in range(N)}
print(allot)

# Function to calculate cost based on top-k preferences
def cost(allot0, pref0):
    score = 0
    for room, person in allot0.items():
        preference_list = []
        for p in pref0:
            if p[0] == person:
                preference_list = p[1]
                break  
        if room in preference_list:
            score += preference_list.index(room)  # Index in top-k preference list
        else:
            score += k  # If room is not in top-k, assign cost k
    return score

# Generate all possible allotments
def generate_permutations(n):
    return list(itertools.permutations(range(n)))

AllPerms = generate_permutations(N)

# Find the best allotment (minimum cost)
bestAllot = {rooms[i]: AllPerms[0][i] for i in range(N)}
bestCost = cost(bestAllot, prefList)

for perm in AllPerms:
    allot = {rooms[i]: perm[i] for i in range(N)}
    newcost = cost(allot, prefList)
    
    print(allot)
    print("Cost:", newcost, "\n")

    if newcost < bestCost:
        bestCost = newcost
        bestAllot = allot

# Print the best allotment
print("\nBest Configuration: ")
print(bestAllot)
print("Minimum Cost:", bestCost)
