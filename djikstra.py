import time
from collections import defaultdict
from minHeap import minHeap
def creategraph(edges):
    for i in range(len(edges)):
        edges[i] = edges[i][::-1]


def dijkstra(edges_with_distances, source, destination):
    #see tests for expected input
    #get Edges in correct format

    edges_from_vertexDict = defaultdict(list)
    for tailnode,headnode,cost in edges_with_distances:
        edges_from_vertexDict[tailnode].append((cost,headnode))

    #Initialize Variables
    seen = set([source])
    #notseen = set([vertices]).remove(source)

    #initialize pathdistance and actual pathdis
    pathdist = {source: 0}
    actualpath = defaultdict(list)
    actualpath[source] = [source]

    #initialize heap
    q = minHeap()
    for edgecost, connectednode in edges_from_vertexDict[source]:
        q.insert((pathdist[source]+edgecost, connectednode, actualpath[source]+[connectednode]))

    while len(q.heapList) != 0:
        (cost,node,path) = q.delmin()
        if node not in seen:
            seen.add(node)
            #notseen.remove(node)
            actualpath[node] = path
            pathdist[node] = cost
            if node == destination:
                return (cost,path)
            for edgecost, connectednode in edges_from_vertexDict[node]:
                if connectednode not in seen:
                    q.insert((pathdist[node]+edgecost,connectednode,actualpath[node]+[connectednode]))
    return float("inf")



if __name__ == "__main__":
    #test 1
    print("test 1")
    timestart = time.time()
    edges = [
        ("A", "B", 7),
        ("A", "D", 5),
        ("B", "C", 8),
        ("B", "D", 9),
        ("B", "E", 7),
        ("C", "E", 5),
        ("D", "E", 15),
        ("D", "F", 6),
        ("E", "F", 8),
        ("E", "G", 9),
        ("F", "G", 11)
    ]

    print("=== Dijkstra ===")
    print(edges)
    print("A -> E:")
    for i in range(10000):
        djiks = dijkstra(edges, "A", "E")
    print(djiks)
    print("time taken = ", time.time() - timestart)
    print("F -> G:")
    print(dijkstra(edges, "F", "G"))

    #test 2
    print("test2")
    from openfile import openAdjListwithWeightsfromFile
    edges = openAdjListwithWeightsfromFile("data/djikstra.txt")
    # report the shortest-path distances from node 1 to the following ten vertices, in order: 7,37,59,82,99,115,133,165,188,197.
    othernodeslist = [7,37,59,82,99,115,133,165,188,197]
    distances = []
    for othernode in othernodeslist:
        distances.append(dijkstra(edges,1,othernode)[0])
    print(distances)
    assert [2599, 2610, 2947, 2052, 2367, 2399, 2029, 2442, 2505, 3068] == distances
    print("assertion passed")
