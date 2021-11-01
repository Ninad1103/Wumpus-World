#!/usr/bin/env python3
from Agent import * # See the Agent.py file
from pysat.solvers import Glucose3

#### All your code can go here.

#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.

#function to find adjacent rooms of current room 
def Adj(currentLocation):
    moves = [[currentLocation[0],currentLocation[1]+1],[currentLocation[0],currentLocation[1]-1],[currentLocation[0]-1,currentLocation[1]],[currentLocation[0]+1,currentLocation[1]]]
    rooms = [] 
    for i in moves :
        if (i[0]>0 and i[0]<5 and i[1]>0 and i[1]<5):
            rooms.append(i)

    return rooms

#mapping assigns the following numbers to our rooms
"""
    [13,14,15,16]
    [9,10,11,12]
    [5,6,7,8]
    [1,2,3,4]

"""

def mapping (currentLocation):
    roomNumber = currentLocation[0] + (currentLocation[1]-1)*4
    return roomNumber  

def main():
    
    ag = Agent()
    knowledgeBase = []
    knowledgeBase.append([16])
    path = []
    
    mineRooms = []
    visited = [] 
    visitCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    prevRoom = 0
    number = 0
    #program terminates after 150 iterations for an invalid minefield
    while (ag.FindCurrentLocation() != [4,4]) :
        safeRooms = []
        currentLocation = ag.FindCurrentLocation()
        visitCount[mapping(currentLocation)-1]+=1
        visited.append(currentLocation)
        path.append(currentLocation)
        knowledgeBase.append([mapping(currentLocation)])
        # [4] in knowledge base means mine is not in room 4 and it is safe 
        percept = ag.PerceiveCurrentLocation()
        adjacentRooms = []
        adjacentRooms = Adj(currentLocation)
        # print("Adjacent Rooms: ",adjacentRooms)
        # print("\n")
        #adding clauses based on percepts
        if percept == '=0' :
            for room in adjacentRooms:
                knowledgeBase.append([mapping(room)])
                if room not in safeRooms:
                    safeRooms.append(room)
        elif percept == '=1':
            if len(adjacentRooms) == 2:
                knowledgeBase.append([-mapping(adjacentRooms[0]), -mapping(adjacentRooms[1])])          
            elif len(adjacentRooms) == 3:
                knowledgeBase.append([-mapping(adjacentRooms[0]), -mapping(adjacentRooms[1]), -mapping(adjacentRooms[2])])
                knowledgeBase.append([mapping(adjacentRooms[0]), mapping(adjacentRooms[1])])
                knowledgeBase.append([mapping(adjacentRooms[1]), mapping(adjacentRooms[2])])
                knowledgeBase.append([mapping(adjacentRooms[2]), mapping(adjacentRooms[0])])    
            elif len(adjacentRooms) == 4:
                knowledgeBase.append([-mapping(adjacentRooms[0]), -mapping(adjacentRooms[1]), -mapping(adjacentRooms[2]),-mapping(adjacentRooms[3])])
                knowledgeBase.append([mapping(adjacentRooms[0]), mapping(adjacentRooms[1])])
                knowledgeBase.append([mapping(adjacentRooms[1]), mapping(adjacentRooms[2])])
                knowledgeBase.append([mapping(adjacentRooms[2]), mapping(adjacentRooms[0])])
                knowledgeBase.append([mapping(adjacentRooms[0]), mapping(adjacentRooms[3])])
                knowledgeBase.append([mapping(adjacentRooms[3]), mapping(adjacentRooms[2])])
                knowledgeBase.append([mapping(adjacentRooms[1]), mapping(adjacentRooms[3])])

        else:
            if len(adjacentRooms) == 2:
                knowledgeBase.append([-mapping(adjacentRooms[0])])
                knowledgeBase.append([-mapping(adjacentRooms[1])])
            elif len(adjacentRooms) == 3:
                knowledgeBase.append([-mapping(adjacentRooms[0]), -mapping(adjacentRooms[1])])
                knowledgeBase.append([-mapping(adjacentRooms[1]), -mapping(adjacentRooms[2])])
                knowledgeBase.append([-mapping(adjacentRooms[2]), -mapping(adjacentRooms[0])])
            elif len(adjacentRooms) == 4:
                knowledgeBase.append([-mapping(adjacentRooms[0]), -mapping(adjacentRooms[1]), -mapping(adjacentRooms[2])])
                knowledgeBase.append([-mapping(adjacentRooms[1]), -mapping(adjacentRooms[3]), -mapping(adjacentRooms[2])])
                knowledgeBase.append([-mapping(adjacentRooms[0]), -mapping(adjacentRooms[3]), -mapping(adjacentRooms[2])])
                knowledgeBase.append([-mapping(adjacentRooms[0]), -mapping(adjacentRooms[1]), -mapping(adjacentRooms[3])])
        
        
        #now to take action TakeAction()
        
        
        g = Glucose3()
        for i in knowledgeBase:
            g.add_clause(i) 
        #checking adjacent rooms by adding clauses and checking safety
        for room in adjacentRooms:  
            if((g.solve(assumptions = [-mapping(room)]) == False) and (room not in safeRooms) ):
                safeRooms.append(room)
                

          
        
        #Searching for action to take in safe rooms 
        #Sorting safe rooms giving more priority to lesser visited rooms 


        # for i in range(len(safeRooms)):
        #     for j in range(i+1,len(safeRooms)):
        #         if (safeRooms[i] in visited and safeRooms[j] not in visited):
        #             safeRooms[i],safeRooms[j] = safeRooms[j],safeRooms[i]           
        
        # for i in range(len(safeRooms)):
        #     for j in range(i+1,len(safeRooms)):
        #         if (visitCount[mapping(safeRooms[i])-1] > visitCount[mapping(safeRooms[j])-1]):
        #             safeRooms[i],safeRooms[j] = safeRooms[j],safeRooms[i]   

        def funcsort (e):
            return visitCount[mapping(e)-1]

        safeRooms.sort(key = funcsort)    
        

        # print("Safe Rooms :", safeRooms)
        # print("\n")
        unvisited = []
        for i in range(len(safeRooms)):
            if (visitCount[mapping(safeRooms[i])-1] == 0):
                unvisited.append(safeRooms[i])
        unvisited.sort(reverse = True)        
        #print("Unvisited :", unvisited)   

        #checking not visited room first to give preference to lesser distance from [4,4]     
        if (len(unvisited) != 0):
            room  = unvisited[0]
            if (mapping(room) - mapping(currentLocation) == 4):
                ag.TakeAction('Up')
                continue
            elif (mapping(room) - mapping(currentLocation) == 1):
                ag.TakeAction('Right')
                continue
            elif (mapping(room) - mapping(currentLocation) == -1):
                ag.TakeAction('Left')
                continue
            elif (mapping(room) - mapping(currentLocation) == -4):
                ag.TakeAction('Down')
                continue   
            print("\n") 
        else:                   
            for room in safeRooms :
                if (mapping(room) - mapping(currentLocation) == 4):
                    ag.TakeAction('Up')
                    break
                elif (mapping(room) - mapping(currentLocation) == 1):
                    ag.TakeAction('Right')
                    break
                elif (mapping(room) - mapping(currentLocation) == -1):
                    ag.TakeAction('Left')
                    break
                elif (mapping(room) - mapping(currentLocation) == -4):
                    ag.TakeAction('Down')
                    break   
                print("\n") 
        number+=1
        if number == 150:
          print("Invalid")
          print("\n")  
          break
        #print("Visted : ",visited)
        #print("\n")         
    path.append([4,4])
    ag.TakeAction('Right')    
    #print(path) 
    for i in range(len(path)-1) :
        print(path[i]," => ",end = '')
    print([4,4])    

if __name__=='__main__':
    main()
