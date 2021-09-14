###### Write Your Library Here ###########
from collections import defaultdict, deque
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

    # BFS를 위한 큐
    queue = deque()
    queue.append(start_point)

    # 이미 방문한 좌표인지 체크하기위한 visit 배열
    visit = [start_point]
    
    # BFS
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

    # Check Path is valid
    isValidPath(path)
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
    # Start and End (Objective) Node
    start = Node(None, start_point)
    end = Node(None, end_point)

    # Open and Close List
    open = []
    close = []

    # Heapify Open List
    hq.heappush(open,start)

    # A*
    while open:
        cur_node = hq.heappop(open)
        close.append(cur_node)

        # End에 도착하면 Path를 찾고 break
        if cur_node == end:
            # Trace Path
            cur = cur_node
            while cur:
                path.append(cur.location)
                cur = cur.parent
            break
        
        
        # Find Next Open Nodes
        for dy,dx in maze.neighborPoints(cur_node.location[0],cur_node.location[1]):
            new_node = Node(cur_node,(dy,dx))
            if new_node in close:
                continue
            new_node.g = cur_node.g + 1
            new_node.h = manhatten_dist(new_node.location, end.location) # heuristic == manhatten_dist
            new_node.f = new_node.g + new_node.h

            for value in open:
                if new_node == value and new_node > value:
                    break
            else:
                hq.heappush(open,new_node)

    
    # Reverse Path
    path = path[::-1]

    # Check Path is valid
    isValidPath(path)
    return path

    ############################################################################


# -------------------- Stage 02: Four circles - A* Algorithm  ------------------------ #



def stage2_heuristic(cur, end, visit):
    # 현재 좌표에서 방문하지 않은 좌표들과의 맨해튼 거리 중 가장 작은 맨해튼 거리를 return
    min_value = float("inf")
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

    # Start Node and End Nodes (Objectives)
    start = Node(None, start_point)
    end = [Node(None, end_point) for end_point in end_points]

    # 도착 좌표를 방문했는지 체크하기위한 visit 배열
    visit = [False for _ in range(len(end_points))]

    for _ in range(4):
        # Initialize Open and Close List at every iteration
        open = []
        close = []

        # iteration이 처음인 경우 == 여태까지 구한 path가 없는 경우
        if len(path) != 0:
            hq.heappush(open,Node(None,path[-1]))
        else:   # 구한 path가 있다면, 마지막 지점부터 다시 시작
            hq.heappush(open,start)

        # A*
        while open:
            cur_node = hq.heappop(open)
            close.append(cur_node)

            # 현재 좌표가 도착 좌표들 중 하나라면 path를 추가
            if cur_node in end:
                if not visit[end.index(cur_node)]: 
                    # 도착 좌표를 방문했다고 체크
                    visit[end.index(cur_node)] = True

                    # Path Trace
                    cur = cur_node
                    tmp = []
                    while cur:
                        tmp.append(cur.location)
                        cur = cur.parent
                    
                    # i-1번째 iteration의 마지막 좌표 ==  i번째 iteration의 첫 좌표
                    # 그렇기에 이전 path에서 [:-1]까지 가져오고 현재 path(tmp)를 reverse하여 추가
                    path = path[:-1] + tmp[::-1]
                    break

            
            # Find Next Open Nodes
            for dy,dx in maze.neighborPoints(cur_node.location[0],cur_node.location[1]):
                new_node = Node(cur_node,(dy,dx))
                if new_node in close:
                    continue
                new_node.g = cur_node.g + 1
                new_node.h = stage2_heuristic(new_node.location, end ,visit) # heuristic == stage2_heuristic
                new_node.f = new_node.g + new_node.h

                for value in open:
                    if new_node == value and new_node > value:
                        break
                else:
                    hq.heappush(open,new_node)

    # Check Path is valid
    isValidPath(path)
    return path
    ############################################################################



# -------------------- Stage 03: Many circles - A* Algorithm -------------------- #

def mst(start, objectives):
    '''
    방문하지 않은 objectives와 현재 노드를 합쳐 mst를 만든다
    각각의 edge들의 weight는 각 edge에서 다른 edge까지의 mahatten 거리를 사용
    mst는 prim 알고리즘을 통해 구현
    '''

    cost_sum=0
    ####################### Write Your Code Here ################################
    
    graph = defaultdict(list)

    # 방문하지않은 각 도착 좌표간의 맨해튼 거리를 구한다
    for y1,x1 in objectives:
        for y2,x2 in objectives:
            if y1 == y2 and x1 == x2:
                continue
            weight = manhatten_dist((y1,x1),(y2,x2))
            graph[(y1,x1)].append((weight, (y2,x2)))
            graph[(y2,x2)].append((weight, (y1,x1)))
    
    # 현재 좌표와 방문하지않은 각 도착 좌표사이의 맨해튼 거리를 구한다
    for y,x in objectives:
        weight = manhatten_dist(start,(y,x))
        graph[(y,x)].append((weight,start))
        graph[start].append((weight,(y,x)))

    # MST 만들기 ( Prim 알고리즘 )
    connected = set([start])
    candidate_edge = graph[start]
    hq.heapify(candidate_edge)
    
    while candidate_edge:
        w, v = hq.heappop(candidate_edge)
        if v not in connected:
            connected.add(v)
            cost_sum += w

            for edge in graph[v]:
                if edge[1] not in connected:
                    hq.heappush(candidate_edge,edge)

    return cost_sum

    ############################################################################


def stage3_heuristic(cur, objectives, visit):
    # cur_node에서 end_node까지 가는 mst를 구축하여, cost_sum을 반환
    not_visit_objectives = []
    
    for idx, objective in enumerate(objectives):
        if not visit[idx]:
            not_visit_objectives.append(objective.location)
    
    return mst(cur,not_visit_objectives)

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
    start_point = maze.startPoint()

    # Start Node and End Nodes (Objectives)
    start = Node(None, start_point)
    end = [Node(None, end_point) for end_point in end_points]

    # 도착 좌표를 방문했는지 체크하기위한 visit 배열
    visit = [False for _ in range(len(end_points))]

    # 모든 도착 좌표를 방문하지 않았을 때까지 iteration
    while visit.count(True) < len(visit):
        # Initialize Open and Close List at every iteration
        open = []
        close = []

        # iteration이 처음인 경우 == 여태까지 구한 path가 없는 경우
        if len(path) != 0:
            hq.heappush(open,Node(None,path[-1]))
        else:   # 구한 path가 있다면, 마지막 지점부터 다시 시작
            hq.heappush(open,start)
        
        # A* 알고리즘
        while open:
            cur_node = hq.heappop(open)
            close.append(cur_node)

            # 현재 좌표가 도착 좌표들 중 하나라면 path를 추가
            if cur_node in end:
                if not visit[end.index(cur_node)]: 
                    # 도착 좌표를 방문했다고 체크
                    visit[end.index(cur_node)] = True

                    # Path Trace
                    cur = cur_node
                    tmp = []
                    while cur:
                        tmp.append(cur.location)
                        cur = cur.parent
                    
                    # i-1번째 iteration의 마지막 좌표 ==  i번째 iteration의 첫 좌표
                    # 그렇기에 이전 path에서 [:-1]까지 가져오고 현재 path(tmp)를 reverse하여 추가
                    path = path[:-1] + tmp[::-1]
                    break

            # Find Next Open Nodes
            for dy,dx in maze.neighborPoints(cur_node.location[0],cur_node.location[1]):
                new_node = Node(cur_node,(dy,dx))
                if new_node in close:
                    continue
                new_node.g = cur_node.g + 1
                new_node.h = stage3_heuristic(new_node.location, end ,visit) # heurisitc == stage3_heuristic
                new_node.f = new_node.g + new_node.h

                for value in open:
                    if new_node == value and new_node > value:
                        break
                else:
                    hq.heappush(open,new_node)
                    
    # Check Path is Valid
    isValidPath(path)
    return path

    ############################################################################

# Check pos1 and pos2 are neighbor
def isNeighbor(pos1,pos2):
    if abs(pos1[0] - pos2[0]) == 0 and abs(pos1[1]-pos2[1]) == 1:
        return True
    elif abs(pos1[0] - pos2[0]) == 1 and abs(pos1[1]-pos2[1]) == 0:
        return True
    return False

# Check Path is valid
def isValidPath(path):
    # 인접한 경로의 좌표가 neighbor가 아니라면 raise Error
    tmp = path[0]
    cnt = 0
    for y,x in path[1:]:
        dy,dx = tmp
        if not isNeighbor((y,x),(dy,dx)):
            cnt += 1
        tmp = (y,x)

    if cnt:
        raise ValueError("올바르지않은 경로로 이동하는 경우가 있습니다.")