from collections import defaultdict
import heapq
# Main Script - Fetch Inputs, do outputs from here. Run directly. 

def main():
    n, m, r = map(int, input().split())
    edgeAdjList = defaultdict(list)
    # defaults to empty list when key hasnt been added
    vertexDistList = defaultdict(int)
    # defaults to "none" when key hasnt been added
    vertexDistList[r] = 0

    for i in range(m):
        u, v, w = map(int, input().split())
        edgeAdjList[u].append((v, w))
        edgeAdjList[v].append((u, w))

    # we have: one iteration on S, one iteration on T
    # it seems necessary to first do a minimum closeness calculation for each vertex
    # and then do a minimum closeness spanning tree on the edges

    # compute a minimum closeness tree for each vertex using the modified Prim's algorithm:
    # O(m log n)
    MSTByVertex(n, r, edgeAdjList, vertexDistList)

    # Using the minimum closeness vertex tree, compute the minimum closeness value of a
    # a spanning tree : O(m log n)
    minAns = minClosenessSpanningTree(n, r, edgeAdjList, vertexDistList)

    # Using the minimum closeness vertex tree, compute the maximum closeness value of 
    # a spanning tree : O(m log n)
    maxAns = maxClosenessSpanningTree(n, r, edgeAdjList, vertexDistList)

    print(f'{minAns} {maxAns}')


def MSTByVertex(n, r, edgeAdjList, vertexDistList):
    """
    Using the modified Prim's algorithm we compute the minimum closeness of each vertex
    and store it in the vertexDistList
    Time Complexity: O(m log m), m = # of edges
        The reheapify each time a new edge is added is O(m log n)
    """
    # set of all vertices in MST
    S = set()
    # adjacent edges to root stored in tuples of their cost
    deltaS = [
        (w + vertexDistList[r], r, v)
        for v, w in edgeAdjList[r]
    ]
    heapq.heapify(deltaS) # O(log m)
    # adding root to MST
    S.add(r)
    # loops through until there are n vertices in S
    while (len(S) != n): # # iterating until all the vertices in tree: O(n)
        # this is the lowest cost edge in delta S
        c, u, v = heapq.heappop(deltaS) # O(log m) (worst case)
        if v not in S:
            # add v to S where v not in S
            S.add(v) 
            vertexDistList[v] = c # set closeness of added vertex
            # add the edges from v to vertices not in S to delta S
            print(f'Adding {v} to S with cost {c} and ans += {vertexDistList[u]}')
            newEdges = [
                (w + vertexDistList[v], v, s)
                for s, w in edgeAdjList[v]
                if s not in S
            ]
            deltaS += newEdges
            heapq.heapify(deltaS)


def minClosenessSpanningTree(n, r, edgeAdjList, vertexDistList):
    """
    Using the modified Prim's algorithm we compute the minimum closeness spanning tree
    We set the weight of each edge as the minimum value of the closeness of their two 
    vertices.
    Time Complexity: O(m log m), m = # of edges
        The reheapify each time a new edge is added is O(m log n)
    """

    # set of vertices in Min Closeness Tree
    T_min = set()
    # Priority queue of edges with weight as the min closeness of their edges
    # initialized to edges adjacent to the root
    deltaT_min = [
        (min(vertexDistList[r],vertexDistList[v]), r, v)
        for v, w in edgeAdjList[r]
    ]
    heapq.heapify(deltaT_min)
    T_min.add(r)
    minAns = 0
    while (len(T_min) != n): # iterating until all the vertices in tree: O(n)
        c, u, v = heapq.heappop(deltaT_min) # this is the lowest dist edge in the graph
        if v not in T_min:
            T_min.add(v) # add to T
            # add the edges from v to vertices not in S to delta S
            minAns += c
            print(f'Adding {v} to T_min with dist {c}')
            # Adds the new edges into Tmin
            newEdges = [
                (min(vertexDistList[v], vertexDistList[s]), v, s)
                for s, w in edgeAdjList[v]
                if s not in T_min
            ]
            deltaT_min += newEdges
            heapq.heapify(deltaT_min)
    return minAns

def maxClosenessSpanningTree(n, r, edgeAdjList, vertexDistList):
    """
    Using the modified Prim's algorithm we compute the maximum closeness spanning tree
    We set the weight of each edge as the minimum value of the closeness of their two 
    vertices. To utilize the prim's algorithm in the same way we did in the minimum 
    spanning tree we invert the values.
    Time Complexity: O(m log m), m = # of edges
        The reheapify each time a new edge is added is O(m log n)
    """
    # set of vertices in Max Closeness Tree
    T_max = set()
    # priority queue of the edges with weight the min closeness of their vertices
    # initialized to just the edges adjacent to the root
    deltaT_max = [
        (min(vertexDistList[r], vertexDistList[v]), r, v)
        for v, w in edgeAdjList[r]
    ]
    heapq.heapify(deltaT_max)
    T_max.add(r)
    maxAns = 0
    while (len(T_max) != n): # iterating until all the vertices in tree: O(n)
        c, u, v = heapq.heappop(deltaT_max) # this is the lowest dist edge in the graph: O(log m)
        if v not in T_max:
            T_max.add(v) # add to T
            maxAns += -c # subtracts the edge weight (inverted for max)
            print(f'Adding {v} to T_max with dist {c}')
            # Adds the new edges into Tmax
            newEdges = [
                (-(min(vertexDistList[v], vertexDistList[s])), v, s)
                for s, w in edgeAdjList[v]
                if s not in T_max
            ]
            deltaT_max += newEdges
            heapq.heapify(deltaT_max)
    
    return maxAns

if __name__ == "__main__":
    main()