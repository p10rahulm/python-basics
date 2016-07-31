from graphObj import Graph
from graphObj import Node
from collections import defaultdict
import time

timestart = time.time()
def DFS(mygraph,source,group = None):
    mygraph.nodes[source].explored = True
    mygraph.nodes[source].layer = 0
    mygraph.nodes[source].group = group
    Q = list([source])
    while len(Q)!=0:
        v = Q.pop(-1)
        for secondnode in mygraph.graph_dict[v]:
            if mygraph.nodes[secondnode].explored == False:
                mygraph.nodes[secondnode].explored = True
                mygraph.nodes[secondnode].group = group
                Q.append(secondnode)
    return mygraph

#below implementation is faster!
def dfs_recursive(mygraph,source,group = None):
    mygraph.nodes[source].explored = True
    mygraph.nodes[source].group = group
    for secondnode in mygraph.graph_dict[source]:
        if mygraph.nodes[secondnode].explored == False:
            dfs_recursive(mygraph,secondnode,group)
    return mygraph

def dfs_recursive_with_label(mygraph,source,label,group = None):
    mygraph.nodes[source].explored = True
    mygraph.nodes[source].group = group
    for secondnode in mygraph.graph_dict[source]:
        if mygraph.nodes[secondnode].explored == False:
            (g,label) = dfs_recursive_with_label(mygraph,secondnode,label,group)
    mygraph.nodes[source].topologicalorder = label
    label -= 1
    return (mygraph,label)

def topologicalsort_dfs_loop(mygraph):
    graph_object = Graph(mygraph)
    label = len(graph_object.nodes)
    for node in graph_object.nodes:
        if graph_object.nodes[node].explored == False:
            dfs_recursive_with_label(graph_object,node,label)
    return [graph_object.nodes[node].topologicalorder for node in graph_object.nodes]

def check_all_vertices_explored(graph,source):
    graph_object = Graph(graph)
    mygraph = (dfs_recursive(graph_object,source))
    for node in mygraph.nodes:
        if mygraph.nodes[node].explored == False:
            print("node not explored = ",node)
            return False
    return True

def find_connected_components(graph):
    graph_object = Graph(graph)
    connected_group = 0
    groups_list =[]
    for node in graph_object.nodes:
        if graph_object.nodes[node].explored==False:
            connected_group += 1
            DFS(graph_object,node,connected_group)
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


    #test2
    print("test 2")
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

    #test3
    print("test 3")
    timestart = time.time()

    g = { 1 : [2,6],
          2 : [5],
          3 : [],
          4 : [1,3],
          5 : [2,4],
          6 : [4]
        }
    for i in range(10000):
        sort_order = topologicalsort_dfs_loop(g)
    print("Time Taken = ",time.time()-timestart, "sort order = ",sort_order)
