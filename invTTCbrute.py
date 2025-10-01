N=5


import random
import copy
# random preference lists

def randomprefgen():
    temp=list(range(N))
    random.shuffle(temp)
    return temp

# person, allotment preference
print("person, allotment pref")
#prefList=[(people[i],randomprefgen()) for i in range(N)]
prefList=[(1, [4,3,2,1,5]), (2, [3,4,1,2,5]), (3,[1,2,3,4,5]), (4, [1,5,3,2,4]), (5, [2,3,4,5,1])]
print(prefList)
finalallot=[4, 3, 1, 5, 2]
finalallot=[4, 3, 2, 1, 5]

prefList_copy = copy.deepcopy(prefList)
# Top trading cycle
def findCycle(pplcycle):
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

def shuffleAllot(cycleList):
    global prefList
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


people=[1,2,3,4,5]

import itertools
def generate_permutations(n):
    elements = list(range(1,n+1))
    permutations = list(itertools.permutations(elements))
    return permutations

ii=0
AllPerms=generate_permutations(N)
for XYZ in AllPerms:
    rooms=XYZ
    allot={rooms[i]:people[i] for i in range(N)}
    prefList=copy.deepcopy(prefList_copy)

    pplleft=set(allot.values())
    origpref=prefList
    while len(prefList)>0:
        cycLi=findCycle(pplleft)
        if len(cycLi)==0:
            break
        pplleft = pplleft.difference({x for y in cycLi for x in y})
        shuffleAllot(cycLi)
        # print("person, allotment pref")
        # print(prefList)
        # print("(rooms,people)")
        # print(allot)
        # print("cost: ",cost(allot,origpref),"\n\n")
        # print("variance",deviation(allot,origpref))
    final_allotment=[next(r for r, p in allot.items() if p == i) for i in range(1, 6)]
    if(final_allotment==finalallot):
        print(rooms)
        ii+=1
    else:
        print("other pareto optimal sol",final_allotment)
    # else:
    #     print(rooms,"->",final_allotment)

print(f"Total ways to get the allotment {finalallot} is",ii)