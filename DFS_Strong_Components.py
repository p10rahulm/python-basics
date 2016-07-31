from graph import Graph
from graph import Node
from collections import defaultdict
import time
from openfile import read_graph_edges_from_file

def DFS_first_pass(mygraph,source,ordering,finishingtime):
    mygraph.nodes[source].explored = True
    Q = list([source])
    dfspath = list([source])
    while len(Q)!=0:
        v = Q.pop(-1)
        iterlist = mygraph.reversedgraph[v]
        for secondnode in iterlist:
            if mygraph.nodes[secondnode].explored == False:
                mygraph.nodes[secondnode].explored = True
                Q.append(secondnode)
                dfspath.append(secondnode)
    for i in dfspath[::-1]:
        finishingtime += 1
        ordering[i] = finishingtime
    return mygraph,ordering,finishingtime

def DFS_second_pass(mygraph,source,leader,leaderlist):
    mygraph.nodes[source].explored = True
    leaderlist[source] = leader
    Q = list([source])
    while len(Q)!=0:
        v = Q.pop(-1)
        iterlist = mygraph.graph_dict[v]
        for secondnode in iterlist:
            if mygraph.nodes[secondnode].explored == False:
                mygraph.nodes[secondnode].explored = True
                leaderlist[secondnode] = leader
                Q.append(secondnode)
    return (mygraph,leaderlist)

def find_strong_components_directed_graph(graph_dictionary):
    #initialize all variables
    mygraph = Graph(graph_dictionary,True)
    size = len(mygraph.nodes)
    finishingtime = 0
    ordering = {}
    leader = None
    leaderlist = {}
    #mygraph.reverse_graph()
    #mygraph.createnodes()
    print("Done Initializing")
    #reverse order of nodes for first pass
    print("no of nodes = ",len(mygraph.nodes.keys()))
    nodesorder  = list(mygraph.nodes.keys())[::-1]
    print("Done Reversing Nodes Order",nodesorder[:10])
    #run dfs for all nodes
    for node in nodesorder:
        if mygraph.nodes[node].explored==False:
            (mygraph,ordering,finishingtime) = DFS_first_pass(mygraph,node,ordering,finishingtime)
    print("Finished DFS First run")
    #get order of nodes rightfor second pass
    nodes = list(mygraph.nodes.keys())
    for node in nodes:        mygraph.nodes[node].explored = False
    nodesorder = [0]*len(nodes)
    for node in nodes:
        nodesorder[ordering[node]-1] = node
    nodesorder = nodesorder[::-1]
    print("Got Nodes order for DFS Second Run", nodesorder[:10])
    for node in nodesorder:
        if mygraph.nodes[node].explored == False:
            leader = node
            (mygraph,leaderlist) = DFS_second_pass(mygraph,node,leader,leaderlist)
    print("Finished DFS Second Run")
    clusters = defaultdict(list)
    for node,group in leaderlist.items():
        clusters[group].append(node)
    clusterlist = []
    for cluster in clusters.keys():
        clusterlist.append((clusters[cluster]))
    clusterlist.sort(reverse=True)
    print("Finished Output")
    return clusterlist


if __name__ == "__main__":

    #test 1
    print("test 1")
    starttime = time.time()
    g = { 1 : [2,6],
          2 : [5],
          3 : [],
          4 : [1,3,4],
          5 : [2,4],
          6 : [4]
        }
    for i in range(10):
        clusters = find_strong_components_directed_graph(g)
    print(clusters)
    clusterlengths = [len(i) for i in clusters]
    clusterlengths.sort(reverse=True)
    print(clusterlengths[:10])

    print("time taken = ",time.time()-starttime)

    #test 2
    print("test 2")
    starttime = time.time()
    g = { 1 : [7],
          2 : [5],
          3 : [9],
          4 : [1],
          5 : [8],
          6 : [3,8],
          7 : [4,9],
          8 : [2],
          9 : [6]
        }
    for i in range(10):
        clusters = find_strong_components_directed_graph(g)
    print("clusters are",clusters)
    print("time taken = ",time.time()-starttime)

    #test 3
    print("test 3 char graph")
    starttime = time.time()
    g = { "1" : ["7"],
          "2" : ["5"],
          "3" : ["9"],
          "4" : ["1"],
          "5" : ["8"],
          "6" : ["3","8"],
          "7" : ["4","9"],
          "8" : ["2"],
          "9" : ["6"]
        }
    for i in range(10):
        clusters = find_strong_components_directed_graph(g)
    print("clusters are",clusters)
    print("time taken = ",time.time()-starttime)

    print("test 3")
    starttime = time.time()
    for i in range(1):
        (g,nedges) = read_graph_edges_from_file("data/scc.txt")
        clusters = find_strong_components_directed_graph(g)
        clusterlengths = [len(i) for i in clusters]
        #mycluster =[i for i in clusters if len(i)==278]
        #print(mycluster)
        clusterlengths.sort(reverse=True)
    print(clusterlengths[:10])


    print("time taken = ",time.time()-starttime)