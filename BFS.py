from graph import Graph
from graph import Node
from queue import Queue
from collections import defaultdict
import time

timestart = time.time()
def BFS(mygraph,source,group = None):
    mygraph.nodes[source].explored = True
    mygraph.nodes[source].layer = 0
    mygraph.nodes[source].group = group
    Q = Queue([source])
    while Q.isempty() == False:
        v = Q.unqueue()
        for secondnode in mygraph.graph_dict[v]:
            if mygraph.nodes[secondnode].explored == False:
                mygraph.nodes[secondnode].explored = True
                mygraph.nodes[secondnode].layer = mygraph.nodes[v].layer + 1
                mygraph.nodes[secondnode].group = group
                Q.enqueue(secondnode)
    return mygraph

def check_all_vertices_explored(graph,source):
    graph_object = Graph(graph)
    mygraph = (BFS(graph_object,source))
    for node in mygraph.nodes:
        if mygraph.nodes[node].explored == False:
            print("node not explored = ",node)
            return False
    return True

def dist(source,dest,graph):
    graph_object = Graph(graph)
    mygraph = (BFS(graph_object,source))
    return mygraph.nodes[dest].layer

def find_connected_components(graph):
    graph_object = Graph(graph)
    connected_group = 0
    groups_list =[]
    for node in graph_object.nodes:
        if graph_object.nodes[node].explored==False:
            connected_group += 1
            BFS(graph_object,node,connected_group)
    result = defaultdict(list)
    for node in graph_object.nodes:
        result[graph_object.nodes[node].group].append(graph_object.nodes[node].id)
    return result

if __name__ == "__main__":
    #test 1
    print("test 1")
    g = { 1 : [2,3,4],
          2 : [1,3,4],
          3 : [1,2,4,5,6],
          4 : [1,2,3, 5,6],
          5 : [3,4],
          6 : [3,4]
        }
    source = 1
    check = True
    for i in range(10000):
        check = check_all_vertices_explored(g,source)
    print("Time Taken = ",time.time()-timestart, "all explored = ",check)


    #test 2
    print("test 2")
    source =1
    dest = 6
    for i in range(10000):
        distance = dist(source,dest,g)
    print("Time Taken = ",time.time()-timestart, "dist = ",distance)

    #test3
    print("test 3")
    timestart = time.time()

    g = { 1 : [3,5],
          2 : [4],
          3 : [1,5],
          4 : [2],
          5 : [1,3,7,9],
          6 : [8,10],
          7 : [5],
          8 : [6,10],
          9 : [5],
          10: [6,8]
        }
    for i in range(10000):
        components = find_connected_components(g)
    print("Time Taken = ",time.time()-timestart, "components = ",components)
