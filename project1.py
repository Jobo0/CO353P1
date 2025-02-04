from collections import defaultdict
import heapq
# Main Script - Fetch Inputs, do outputs from here. Run directly. 

def main():
    minAns = 0
    maxAns = 0
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
    # first while: is like a minimum closeness spanning tree, except it's minimizing the closeness on the vertices
    #               and not the edges. Stores the closness of each vertex in vertexDistList
    # second while: this is prim's algorithm, but the edge weights are set to be their closeness
    #               aka min(vertexDistList[u], vertexDistList[v])
    # time complexity analysis:
    # 
    S = set()
    deltaS = [
        (w + vertexDistList[r], r, v)
        for v, w in edgeAdjList[r]
    ]
    heapq.heapify(deltaS)
    S.add(r)
    while (len(S) != n):
        c, u, v = heapq.heappop(deltaS) # this is the lowest cost edge in delta S
        if v not in S:
            S.add(v) # add to S
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


    T = set()
    deltaT = [
        (min(vertexDistList[r],vertexDistList[v]), r, v)
        for v, w in edgeAdjList[r]
    ]
    heapq.heapify(deltaT)
    T.add(r)
    while (len(T) != n):
        c, u, v = heapq.heappop(deltaT) # this is the lowest dist edge in the graph
        if v not in T:
            T.add(v) # add to T
            # add the edges from v to vertices not in S to delta S
            minAns += c
            print(f'Adding {v} to T with dist {c}')
            newEdges = [
                (min(vertexDistList[v], vertexDistList[s]), v, s)
                for s, w in edgeAdjList[v]
                if s not in T
            ]
            deltaT += newEdges
            heapq.heapify(deltaT)

    print(f'{minAns} {maxAns}')

if __name__ == "__main__":
    main()