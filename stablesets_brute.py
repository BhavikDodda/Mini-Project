

import time
import random
import copy
start = time.time()

# random preference lists

def randomprefgen():
    temp=list(range(N))
    random.shuffle(temp)
    return temp

# person, allotment preference
print("person, allotment pref")
#prefList=[(people[i],randomprefgen()) for i in range(N)]
prefList=[(1, [4,3,2,1,5]), (2, [3,4,1,2,5]), (3,[1,2,3,4,5]), (4, [1,5,3,2,4]), (5, [2,3,4,5,1])]
import pickle

with open("prefList.pkl", "rb") as f:
    prefList = pickle.load(f)
print(prefList)
prefDict = dict(prefList)
N=len(prefList)

prefList_copy = copy.deepcopy(prefList)
# Top trading cycle
def findCycle(pplcycle,allot,prefList):
    cycleList=[]
    leftout=pplcycle
    while leftout:
        startperson=next(iter(leftout))
        iterperson=startperson

        cycle=[iterperson]
        while True:
            iterperson=allot[[item for item in prefList if item[0]==iterperson][0][1][0]]
            if(iterperson==startperson):
                leftout=leftout.difference(set(cycle))
                cycleList.append(cycle)
                break
            if iterperson in cycle:
                cycle=cycle[cycle.index(iterperson):]
                leftout=leftout.difference(set(cycle))
                cycleList.append(cycle)
                break
            elif iterperson not in leftout:
                leftout.remove(startperson)
                break
            cycle.append(iterperson)
        
    #print("list of ppl that need to cycle", cycleList)
    return cycleList

def shuffleAllot(cycleList,allot,prefList):
    for thecycle in cycleList:
        rooms=[[item for item in prefList if item[0]==i][0][1][0] for i in thecycle]
        for room, person in zip(rooms, thecycle):
            allot[room] = person
        def filter0(item0):
            return item0[0] not in thecycle
        prefList=list(filter(filter0,prefList))
        def filter1(item1):
            return item1 not in rooms
        newprefList=[]
        for personslist in prefList:
            newprefList.append((personslist[0],list(filter(filter1,personslist[1]))))
        prefList=newprefList
    return prefList
        
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

def ttc(rooms):
    allot={rooms[i]:people[i] for i in range(N)}
    prefList=copy.deepcopy(prefList_copy)

    pplleft=set(allot.values())
    origpref=prefList
    while len(prefList)>0:
        cycLi=findCycle(pplleft,allot,prefList)
        if len(cycLi)==0:
            break
        pplleft = pplleft.difference({x for y in cycLi for x in y})
        prefList=shuffleAllot(cycLi,allot,prefList)
        # print("person, allotment pref")
        # print(prefList)
        # print("(rooms,people)")
        # print(allot)
        # print("cost: ",cost(allot,origpref),"\n\n")
        # print("variance",deviation(allot,origpref))
    solution=[next(r for r, p in allot.items() if p == i) for i in range(1, N+1)]
    return solution


import itertools
def generate_permutations(n):
    elements = tuple(range(1,n+1))
    permutations = list(itertools.permutations(elements))
    return permutations


people=list(range(1,N+1))
pareto_optimal=set()

for roomList in generate_permutations(N):
    pareto_optimal.add(tuple(ttc(roomList)))

print("pareto optimal list",list(pareto_optimal))
print("Total pareto optimal solutions found:",len(pareto_optimal))

end = time.time()
print("Time taken:", end - start, "seconds")