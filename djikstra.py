import time
from collections import defaultdict
from binHeap import minHeap
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
    for i in range(100000):
        djiks = dijkstra(edges, "A", "E")
    print(djiks)
    print("time taken = ", time.time() - timestart)
    print("F -> G:")
    print(dijkstra(edges, "F", "G"))