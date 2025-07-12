N=5
rooms=list(range(N))
people=list(range(N))

import random
# random preference lists
def randomprefgen():
    temp=list(range(N))
    random.shuffle(temp)
    return temp

# person, allotment preference
print("person, allotment pref")
#prefList=[(people[i],randomprefgen()) for i in range(N)]
#prefList=[(0, [0, 1, 3, 2, 4]), (1, [2, 0, 3, 4, 1]), (2, [2, 1, 0, 4, 3]), (3, [1, 3, 2, 0, 4]), (4, [1, 0, 3, 2, 4])]
""" prefList = [
    (0, [4,1,2,0,3]),  # Person 1's preference order
    (1,[1,3,0,4,2]),  # Person 2's preference order
    (2,[1,0,4,2,3]),  # Person 3's preference order
    (3,[3,1,2,0,4]),  # Person 4's preference order
    (4,[1,0,2,3,4])   # Person 5's preference order
] """
prefList=[
    (0, [0,2,1,3,4]),  # Person 1's preference order
    (1,[4,3,0,1,2]),  # Person 2's preference order
    (2,[2,1,4,0,3]),  # Person 3's preference order
    (3,[1,4,3,2,0]),  # Person 4's preference order
    (4,[1,2,4,3,0])   # Person 5's preference order
]
print(prefList)

# random allotment (room,person)
print("(rooms,people)")
random.shuffle(people)
#allot={rooms[i]:people[i] for i in range(N)}
allot={0: 1, 1: 0, 2: 3, 3: 2, 4: 4}
print(allot)
        
def cost(allot0,pref0):
    score=0
    for room in allot0:
        person=allot0[room]
        score+=[item for item in pref0 if item[0]==person][0][1].index(room)
    return score

import itertools
def generate_permutations(n):
    elements = list(range(n))
    permutations = list(itertools.permutations(elements))
    return permutations

AllPerms=generate_permutations(N)
bestAllot=[{rooms[i]:(AllPerms[0])[i] for i in range(N)}]
bestCost=cost(bestAllot[0],prefList)
for ii in AllPerms:
    allot={rooms[i]:ii[i] for i in range(N)}
    newcost=cost(allot,prefList)
    print(allot)
    print(newcost,"\n")

    if(newcost<bestCost):
        bestCost=newcost
        bestAllot=[allot]
    if(newcost==bestCost):
        if(allot not in bestAllot):
            bestAllot.append(allot)

print("#######\nMinima: ")
print(bestAllot)
print(bestCost)