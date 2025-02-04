import sys
from collections import defaultdict

class GraphOneTrees: # Disjoint set structure for identifying one-tree graph components
    def __init__(self, n):
        self.parent = {i: i for i in range(n)}  # Parent reference gives tree association

    def find(self, x): # Root parent gives lowest indexed node in one-tree
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            if root_x < root_y:
                self.parent[root_y] = root_x
            else:
                self.parent[root_x] = root_y

def find_forest(n, edges):
    got = GraphOneTrees(n)
    
    for a, b in edges:
        got.union(a, b)

    # Group nodes by root parent
    forest = defaultdict(list)
    for node in range(n):
        root = got.find(node)
        forest[root].append(node)

    return list(forest.values())

def cheapest_subtree(k, one_trees):
    weight = k # Min -> all of length 1

    one_trees.sort(key = len, reverse = True) # fine within time complexity O(nlogn) < O(m)

    # Connect components by adding one to weight (using 2 edge)
    # until we connect sufficient nodes
    connect_nodes = k + 1 # k edges connect k+1 nodes
    nodes_connected = len(one_trees[0])
    connect_component = 1
    while (nodes_connected < connect_nodes):
        weight += 1 # swap a 1 edge with a 2 edge
        nodes_connected += len(one_trees[connect_component])
        # won't be out of range unless k > n
        connect_component += 1

    return weight

def main():
    n, k = map(int, sys.stdin.readline().strip().split())
    one_edges = []
    for line in sys.stdin:
        a, b, w = map(int, line.strip().split())
        if (w == 1):
            one_edges.append((a, b))
    
    # Get connected components
    one_trees = find_forest(n, one_edges)
    
    # Get min-weight sub tree from one-trees
    print(cheapest_subtree(k, one_trees))
    

if __name__ == "__main__":
    main()
