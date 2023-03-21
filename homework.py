#!/usr/bin/env python
# coding: utf-8

# In[1]:


from heapq import heappush,heappop
import math


# In[2]:


locationOftheGrid=[]
availableMoves={} 
visitedGrid={}
with open('input8.txt') as f:
    lines = f.readlines()
    algorithmName=lines[0].rstrip('\n')
    boundary=tuple(int(num) for num in lines[1].rstrip('\n').split(' '))
    start=tuple(int(num) for num in lines[2].rstrip('\n').split(' '))
    end=tuple(int(num) for num in lines[3].rstrip('\n').split(' '))
    noOfGrids=int(lines[4].rstrip('\n'))
    locationOftheGrid=[]
    for i in range(noOfGrids):
        splitLine=lines[5+i].rstrip('\n').split(' ')
        locationOftheGrid.append(tuple(int(num) for num in splitLine[0:3]))
        visitedGrid[locationOftheGrid[i]]=0
        availableMoves[locationOftheGrid[i]]=list(int(num) for num in splitLine[3:])

        


# In[3]:


def doAction(actionNumber,location):
    if actionNumber==1:
        location[0]+=1
    elif actionNumber==2:
        location[0]-=1
    elif actionNumber==3:
        location[1]+=1
    elif actionNumber==4:
        location[1]-=1
    elif actionNumber==5:
        location[2]+=1
    elif actionNumber==6:
        location[2]-=1
    elif actionNumber==7:
        location[0]+=1
        location[1]+=1
    elif actionNumber==8:
        location[0]+=1
        location[1]-=1
    elif actionNumber==9:
        location[0]-=1
        location[1]+=1
    elif actionNumber==10:
        location[0]-=1
        location[1]-=1
    elif actionNumber==11:
        location[0]+=1
        location[2]+=1
    elif actionNumber==12:
        location[0]+=1
        location[2]-=1
    elif actionNumber==13:
        location[0]-=1
        location[2]+=1
    elif actionNumber==14:
        location[0]-=1
        location[2]-=1
    elif actionNumber==15:
        location[1]+=1
        location[2]+=1
    elif actionNumber==16:
        location[1]+=1
        location[2]-=1
    elif actionNumber==17:
        location[1]-=1
        location[2]+=1
    elif actionNumber==18:
        location[1]-=1
        location[2]-=1
    return location


# In[4]:


doAction(6,list((5,3,5)))


# In[5]:


def checkBoundary(currentLocation):
    if currentLocation[0]<0 or currentLocation[1]<0 or currentLocation[2]<0 or currentLocation[0]>boundary[0] or currentLocation[1]>boundary[1] or currentLocation[2]>boundary[2] : return False
    return True


# In[6]:


checkBoundary([11,10,1])


# In[7]:


def startBreadthFirstSearch(rootNode):
    queue=[]
    path={}
    queue.append(rootNode)
    flag=0
    if not checkBoundary(rootNode) : return {}
    if rootNode==end : return {rootNode:0}
    while queue:
        currentNode=queue.pop(0)
        if currentNode in availableMoves and visitedGrid[currentNode]==0:
            visitedGrid[currentNode]=1
            availableMoveForCureentNode=availableMoves[currentNode]
            for index in range(len(availableMoveForCureentNode)):
                nextNode=doAction(availableMoveForCureentNode[index],list(currentNode))
                nextNode=tuple(nextNode)
                if checkBoundary(nextNode) and nextNode not in path and visitedGrid[nextNode]==0:
                    path[nextNode]=currentNode
                    queue.append(nextNode)
                if nextNode==end:
                    flag=1
                    return path
    if flag==0:
        return {}


# In[8]:


def costBasedOnAction(actionNumber):
    if actionNumber>=0 and actionNumber<=6:
        return 10
    elif actionNumber>6 and actionNumber<=18:
        return 14


# In[9]:


costBasedOnAction(12)


# In[10]:


def startUnifromCostSearch(rootNode):
    queue=[]
    path={}
    searchCost=0
    flag=0
    costDict={rootNode:0}
    costList={rootNode:0}
    costToInfinity=99999999999999
    heappush(queue, [searchCost ,rootNode])
    if not checkBoundary(rootNode) : return [0,{},{}]
    if rootNode==end : return [0,costList,costDict]
    while queue:       
        currentNodeInHeap=heappop(queue)
        searchCost=currentNodeInHeap[0]
        currentNode=currentNodeInHeap[1]
        if currentNode in costDict and costDict[currentNode]<searchCost: continue
        if currentNode==end and costToInfinity>=searchCost+nextCost:
            flag=1
            return [searchCost,costList,path]
        if currentNode in availableMoves and visitedGrid[currentNode]==0:
            visitedGrid[currentNode]=1
            availableMoveForCureentNode=availableMoves[currentNode]
            for index in range(len(availableMoveForCureentNode)):
                nextNode=doAction(availableMoveForCureentNode[index],list(currentNode))
                nextNode=tuple(nextNode)
                nextCost=costBasedOnAction(availableMoveForCureentNode[index])
                if nextNode in path and costDict[nextNode]>searchCost+nextCost:
                    costDict[nextNode]=searchCost+nextCost
                    costList[nextNode]=nextCost
                    heappush(queue, [searchCost+nextCost,nextNode])
                if checkBoundary(nextNode) and nextNode not in path and visitedGrid[nextNode]==0:
                    path[nextNode]=currentNode
                    costDict[nextNode]=searchCost+nextCost
                    costList[nextNode]=nextCost
                    heappush(queue,[searchCost+nextCost,nextNode])
    if flag==0:
        return [0,{},{}]


# In[11]:


def aStarHeuristic(location):
    return math.sqrt(abs(location[0]-end[0])**2 + abs(location[1]-end[1])**2 + abs(location[2]-end[2])**2)


# In[12]:


aStarHeuristic(start)


# In[13]:


def startAStarSearch(rootNode):
    queue=[]
    path={}
    searchCost=0
    flag=0
    costDict={rootNode:0}
    costList={rootNode:0}
    costToInfinity=9999999999999999
    aSearchCost=aStarHeuristic(rootNode)
    heappush(queue, [aSearchCost,searchCost, rootNode])
    if not checkBoundary(rootNode) : return [0,{},{}]
    if rootNode==end : return [0,costList,costDict]
    while queue:
        currentNodeInHeap=heappop(queue)
        aSearchCost=currentNodeInHeap[0]
        searchCost=currentNodeInHeap[1]
        currentNode=currentNodeInHeap[2]
        if currentNode in costDict and costDict[currentNode]<searchCost: continue
        if currentNode==end and costToInfinity>=searchCost+aSearchCost+nextCost:
            flag=1
            return [searchCost,costList,path]
        if currentNode in availableMoves and visitedGrid[currentNode]==0:
            visitedGrid[currentNode]=1
            availableMoveForCureentNode=availableMoves[currentNode]
            for index in range(len(availableMoveForCureentNode)):
                nextNode=doAction(availableMoveForCureentNode[index],list(currentNode))
                nextNode=tuple(nextNode)
                nextCost=costBasedOnAction(availableMoveForCureentNode[index])
                nextASearchCost=aStarHeuristic(nextNode)
                if nextNode in path and costDict[nextNode]>searchCost+nextCost+nextASearchCost:
                    print(nextNode)
                    costDict[nextNode]=searchCost+nextCost+nextASearchCost
                    costList[nextNode]=nextCost
                    heappush(queue, [searchCost+nextCost+nextASearchCost,searchCost+nextCost, nextNode])
                if visitedGrid[nextNode]==0 and checkBoundary(nextNode) and nextNode not in path:
                    path[nextNode]=currentNode
                    costDict[nextNode]=searchCost+nextCost+nextASearchCost
                    costList[nextNode]=nextCost
                    heappush(queue, [searchCost+nextCost+nextASearchCost,searchCost+nextCost,nextNode])
    if flag==0:
        return [0,{},{}]


# In[14]:


def outputSearch(algorithmName,path,cost,costList):
    f = open("output.txt","w")
    if path == []:
        f.write("FAIL")
    else:
        f.write(str(cost)+"\n")
        numberOfNodes=len(path)
        f.write(str(numberOfNodes)+"\n")
        for i in range(len(path)):
            currentCost=0
            if(algorithmName=="BFS"):
                currentCost=costList[i]
            elif algorithmName=="UCS" or algorithmName=="A*":
                currentCost=costList[path[i]]
            if i==(len(path)-1):
                f.write(str(path[i][0])+" "+str(path[i][1])+" "+str(path[i][2])+" "+str(currentCost))
            else:
                f.write(str(path[i][0])+" "+str(path[i][1])+" "+str(path[i][2])+" "+str(currentCost)+"\n")


# In[15]:


def getPath(pathSpace,rootNode):
    path=[]
    if len(pathSpace)==0: return path
    else:
        if rootNode==end:
            path.append(rootNode)
            return path
        else:
            currentNode=end
            path.append(currentNode)
            while currentNode!=rootNode:
                nextNode=pathSpace[currentNode]
                path.append(nextNode)
                currentNode=nextNode
            path.reverse()
            return path


# In[16]:


def startSearch(algorithmName,rootNode):
    if algorithmName=="BFS":
        pathSpace=startBreadthFirstSearch(rootNode)
        path=getPath(pathSpace,rootNode)
        if len(path)>0:
            searchCost=len(path)-1
            costList=[1]*len(path)
            costList[0]=0
        else:
            searchCost=0
            costList=[]
        outputSearch(algorithmName,path,searchCost,costList)
    elif algorithmName=="UCS":
        searchCost,costList,pathSpace=startUnifromCostSearch(rootNode)
        path=getPath(pathSpace,rootNode)
        outputSearch(algorithmName,path,searchCost,costList)
    elif algorithmName=="A*":
        searchCost,costList,pathSpace=startAStarSearch(rootNode)
        path=getPath(pathSpace,rootNode)
        outputSearch(algorithmName,path,searchCost,costList)


# In[17]:


startSearch(algorithmName,start)


# In[ ]:





# In[ ]:




