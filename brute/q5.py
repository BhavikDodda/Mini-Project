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
prefList=[(0, [0, 1, 3, 2, 4]), (1, [2, 0, 3, 4, 1]), (2, [3, 1, 0, 4, 2]), (3, [1, 3, 2, 0, 4]), (4, [4, 0, 3, 2, 1])]
print(prefList)

# random allotment (room,person)
print("(rooms,people)")
random.shuffle(people)
#allot={rooms[i]:people[i] for i in range(N)}
allot={0: 1, 1: 0, 2: 3, 3: 2, 4: 4}
#print(allot)
        
def cost(allot0,pref0):
    score=0
    for room in allot0:
        person=allot0[room]
        score+=[item for item in pref0 if item[0]==person][0][1].index(room)
    return score

def deviation(allot0,pref0):
    avg=cost(allot0,pref0)/N
    dev=0
    for room in allot0:
        person=allot0[room]
        dev+=([item for item in pref0 if item[0]==person][0][1].index(room)-avg)**2
    return dev

import itertools
def generate_permutations(n):
    elements = list(range(n))
    permutations = list(itertools.permutations(elements))
    return permutations

AllPerms=generate_permutations(N)
bestAllot={rooms[i]:(AllPerms[0])[i] for i in range(N)}
#print(bestAllot)
bestDev=deviation(bestAllot,prefList)

for i in range(N):
    possible=set([item[1][i] for item in prefList])
    print("possible",possible)
    if(len(possible)==N):
        print(i)
        newAllot={prefList[j][1][i]:prefList[j][0] for j in range(N)}
        print(bestAllot)
        newDev=deviation(newAllot,prefList)
        if newDev<bestDev:
            bestDev=newDev
            bestAllot=newAllot

print("#######\nMinima: ")
print(bestAllot)
print(bestDev)