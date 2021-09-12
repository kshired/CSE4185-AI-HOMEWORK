###### Write Your Library Here ###########
from collections import deque
import heapq as hq
#########################################


def search(maze, func):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_four_circles": astar_four_circles,
        "astar_many_circles": astar_many_circles
    }.get(func)(maze)


# -------------------- Stage 01: One circle - BFS Algorithm ------------------------ #

def bfs(maze):
    """
    [문제 01] 제시된 stage1의 맵 세가지를 BFS Algorithm을 통해 최단 경로를 return하시오.(20점)
    """
    start_point = maze.startPoint()

    ####################### Write Your Code Here ################################

    # End point
    end_point = maze.circlePoints()[0]

    # Tracing을 위한 Set
    prev = {}

    queue = deque()
    queue.append(start_point)
    visit = [start_point]
    
    while queue:
        y,x = queue.popleft()
        if (y,x) == end_point:
            break
        for dy,dx in maze.neighborPoints(y,x):
            if (dy,dx) not in visit:
                visit.append((dy,dx))
                queue.append((dy,dx))
                prev[(dy,dx)] = (y,x)

    # Trace path
    node = (y,x)
    path = [node]

    while node != start_point:
        node = prev[node]
        path.append(node)

    return path[::-1]
    ############################################################################



class Node:
    def __init__(self,parent,location):
        self.parent=parent
        self.location=location #현재 노드

        self.obj=[]

        # F = G+H
        self.f=0
        self.g=0
        self.h=0

    def __eq__(self, other):
        return self.location==other.location and str(self.obj)==str(other.obj)

    def __le__(self, other):
        return self.g+self.h<=other.g+other.h

    def __lt__(self, other):
        return self.g+self.h<other.g+other.h

    def __gt__(self, other):
        return self.g+self.h>other.g+other.h

    def __ge__(self, other):
        return self.g+self.h>=other.g+other.h


# -------------------- Stage 01: One circle - A* Algorithm ------------------------ #

def manhatten_dist(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def astar(maze):

    """
    [문제 02] 제시된 stage1의 맵 세가지를 A* Algorithm을 통해 최단경로를 return하시오.(20점)
    (Heuristic Function은 위에서 정의한 manhatten_dist function을 사용할 것.)
    """

    start_point=maze.startPoint()

    end_point=maze.circlePoints()[0]

    path=[]

    ####################### Write Your Code Here ################################
    start = Node(None, start_point)
    end = Node(None, end_point)

    open = []
    close = []
    hq.heappush(open,start)

    while open:
        cur_node = hq.heappop(open)
        close.append(cur_node)

        if cur_node == end:
            cur = cur_node
            while cur:
                path.append(cur.location)
                cur = cur.parent
            break
        
        children = []

        for dy,dx in maze.neighborPoints(cur_node.location[0],cur_node.location[1]):
            new_node = Node(cur_node,(dy,dx))
            children.append(new_node)

        for child in children:
            if child in close:
                continue
            child.g = cur_node.g + 1
            child.h = manhatten_dist(child.location, end.location)
            child.f = child.g + child.h

            for value in open:
                if child == value and child > value:
                    break
            else:
                hq.heappush(open,child)
                
    path = path[::-1]
    return path

    ############################################################################


# -------------------- Stage 02: Four circles - A* Algorithm  ------------------------ #



def stage2_heuristic(cur, end, visit):
    min_value = 1e9+7
    for idx,end_point in enumerate(end):
        if not visit[idx]:
            min_value = min(min_value,manhatten_dist(cur,end_point.location))
    return min_value


def astar_four_circles(maze):
    """
    [문제 03] 제시된 stage2의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage2_heuristic function을 직접 정의하여 사용해야 한다.)
    """

    end_points=maze.circlePoints()
    end_points.sort()

    path=[]

    ####################### Write Your Code Here ################################
    start_point = maze.startPoint()

    start = Node(None, start_point)
    end = [Node(None, end_point) for end_point in end_points]
    visit = [False for _ in range(len(end_points))]

    for _ in range(4):
        open = []
        close = []
        if len(path) != 0:
            hq.heappush(open,Node(None,path[-1]))
        else:
            hq.heappush(open,start)
        while open:
            cur_node = hq.heappop(open)
            close.append(cur_node)

            if cur_node in end:
                if not visit[end.index(cur_node)]: 
                    visit[end.index(cur_node)] = True
                    cur = cur_node
                    tmp = []
                    while cur:
                        tmp.append(cur.location)
                        cur = cur.parent
                    path = path[:-1] + tmp[::-1]
                    break

            children = []

            for dy,dx in maze.neighborPoints(cur_node.location[0],cur_node.location[1]):
                new_node = Node(cur_node,(dy,dx))
                children.append(new_node)

            for child in children:
                if child in close:
                    continue
                child.g = cur_node.g + 1
                child.h = stage2_heuristic(child.location, end, visit)
                child.f = child.g + child.h

                for value in open:
                    if child == value and child > value:
                        break
                else:
                    hq.heappush(open,child)

    # def isNeighbor(pos1,pos2):
    #     if abs(pos1[0] - pos2[0]) == 0 and abs(pos1[1]-pos2[1]) == 1:
    #         return True
    #     elif abs(pos1[0] - pos2[0]) == 1 and abs(pos1[1]-pos2[1]) == 0:
    #         return True
    #     return False

    # dir = [(0,1),(1,0),(-1,0),(0,-1)]

    # tmp = path[0]
    # cnt = 0
    # for y,x in path[1:]:
    #     dy,dx = tmp
    #     if not isNeighbor((y,x),(dy,dx)):
    #         cnt += 1
    #     tmp = (y,x)

    # print(cnt)
    return path
    ############################################################################



# -------------------- Stage 03: Many circles - A* Algorithm -------------------- #

def mst(objectives, edges):

    cost_sum=0
    ####################### Write Your Code Here ################################













    return cost_sum

    ############################################################################


def stage3_heuristic():
    pass


def astar_many_circles(maze):
    """
    [문제 04] 제시된 stage3의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage3_heuristic function을 직접 정의하여 사용해야 하고, minimum spanning tree
    알고리즘을 활용한 heuristic function이어야 한다.)
    """

    end_points= maze.circlePoints()
    end_points.sort()

    path=[]

    ####################### Write Your Code Here ################################





















    return path

    ############################################################################
