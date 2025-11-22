PRINT_INFO=False

import random
import copy
import time
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
import os
with open(os.path.join(os.path.dirname(__file__), "prefList.pkl"), "rb") as f:
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




def dressup(taggedAllotment, doneRooms):
    newTagged = []
    for idx, (room, tag) in enumerate(taggedAllotment):
        if tag == 1:
            newTagged.append((room, 1))
        elif tag == -1:
            person = people[idx]
            # filter out doneRooms
            prefs = [r for r in prefDict[person] if r not in doneRooms]
            if prefs and prefs[0] == room:
                newTagged.append((room, 0))
            else:
                newTagged.append((room, -1))
        else:
            newTagged.append((room, tag))
    return newTagged


from itertools import permutations
from collections import deque

def all_squares(tagged):
    return all(tag == 1 for _, tag in tagged)

def devour(initial):
    results = []
    visited = set()
    q = deque([tuple(initial)])  # store as immutable

    while q:
        state = q.popleft()
        if state in visited:
            continue
        visited.add(state)

        if all_squares(state):
            results.append(state)
            continue

        # Extract
        rooms = [r for r, _ in state]
        tags  = [t for _, t in state]

        # indices of circle tags
        circle_idx = [i for i,t in enumerate(tags) if t == 0]
        circle_rooms = [rooms[i] for i in circle_idx]

        # generate permutations of circle rooms
        for perm in set(permutations(circle_rooms)):
            new_rooms = list(rooms)
            new_tags = tags[:]
            for idx, val in zip(circle_idx, perm):
                if val!=new_rooms[idx]:
                    new_tags[idx] = 1
                new_rooms[idx] = val
        
            # rebuild tagged state
            new_state = [(r,t) for r,t in zip(new_rooms,new_tags)]
            doneRooms = [r for r,t in new_state if t == 1]
            dressed = dressup(new_state, doneRooms)
            q.append(tuple(dressed))
        for idxx in circle_idx:
            new_rooms = list(rooms)
            new_tags = tags[:]
            new_tags[idxx] = 1 
            new_state = [(r,t) for r,t in zip(new_rooms,new_tags)]
            doneRooms = [r for r,t in new_state if t == 1]
            dressed = dressup(new_state, doneRooms)
            q.append(tuple(dressed))
    results_extracted=[tuple(r for r,t in state) for state in results]
    return results_extracted
pareto_optimal=[]
pareto_optimal_inv=[]
people=list(range(1,N+1))


scan=(set(generate_permutations(N)))

while scan:
    rooms=scan.pop()
    finalallot=ttc(rooms)
    if(finalallot not in pareto_optimal):
        pareto_optimal.append(finalallot)

        initFinalAllot = [(room, -1) for room in finalallot]
        all_initials = devour(dressup(initFinalAllot, []))

        all_initials_sorted = sorted(all_initials)
        pareto_optimal_inv.append(all_initials_sorted)
        if PRINT_INFO: print("New Pareto optimal found:",finalallot," from initial allotment ",rooms)
        if PRINT_INFO: print("Total pareto optimal solutions found till now:",len(pareto_optimal),". Inverse contains: ",len(all_initials_sorted),"\n")
        # remove all permutations giving same final allotment
        scan=scan.difference(set(all_initials_sorted))
    else:
        if PRINT_INFO: print("Already found pareto optimal",finalallot," from initial allotment ",rooms)

if PRINT_INFO: print("pareto optimal list",pareto_optimal)
if PRINT_INFO: print("Total pareto optimal solutions found:",len(pareto_optimal))
pareto_optimal_first=copy.deepcopy(pareto_optimal)


end = time.time()
if PRINT_INFO: print("Time taken:", end - start, "seconds")

###################################



import time
import random
import copy
start2 = time.time()

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
import os
with open(os.path.join(os.path.dirname(__file__), "prefList.pkl"), "rb") as f:
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

if PRINT_INFO: print("pareto optimal list",list(pareto_optimal))
if PRINT_INFO: print("Total pareto optimal solutions found:",len(pareto_optimal))

end2 = time.time()
if PRINT_INFO: print("Time taken:", end2 - start2, "seconds")


from logStuff import log_stats
log_stats("INVTTC vs BRUTE", prefList,pareto_optimal_first,pareto_optimal, start, end, start2, end2)
#(method_name, prefList, num_pareto1, num_pareto2, start_time, end_time, start_time2, end_time2)