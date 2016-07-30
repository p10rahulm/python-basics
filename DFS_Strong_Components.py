from graph import Graph
from graph import Node
from collections import defaultdict
import time


def dfs_pass_looper(mygraph,ordering,finishingtime,leader,leaderlist,passnumber):
    if passnumber == 1:
        nodesorder  = list(mygraph.nodes.keys())[::-1]
        mygraph.getsource_dest_nodes()
    else:
        nodes = list(mygraph.nodes.keys())
        nodesorder = [0]*len(nodes)
        for node in nodes:
            nodesorder[ordering[node]-1] = node
        nodesorder = nodesorder[::-1]
    for node in nodesorder:
        if mygraph.nodes[node].explored == False:
            if passnumber == 2: leader = node
            (mygraph,ordering,finishingtime,leader,leaderlist) = dfs_DAG(mygraph,node,leader,leaderlist,ordering,finishingtime,passnumber)
    return (mygraph,ordering,finishingtime,leader,leaderlist)



def dfs_DAG(mygraph,source,leader,leaderlist,ordering,finishingtime,passnumber):
    mygraph.nodes[source].explored = True
    if passnumber == 2: leaderlist[source] = leader
    if passnumber == 1:
        iterlist = [mygraph.sourcenodes[i] for i in range(len(mygraph.destnodes)) if mygraph.destnodes[i] == source]
    else:
        iterlist = mygraph.graph_dict[source]

    for secondnode in iterlist:
        if mygraph.nodes[secondnode].explored != True:
            (mygraph,ordering,finishingtime,leader,leaderlist) = dfs_DAG(mygraph,secondnode,leader,leaderlist,ordering,finishingtime,passnumber)

    if passnumber ==1:
        finishingtime += 1
        ordering[source] = finishingtime
    return (mygraph,ordering,finishingtime,leader,leaderlist)



def find_strong_components_directed_graph(graph_dictionary):
    mygraph = Graph(graph_dictionary)
    size = len(mygraph.nodes)
    finishingtime = 0
    ordering = {}
    leader = None
    leaderlist = {}
    (mygraph,ordering,finishingtime,leader,leaderlist) = dfs_pass_looper(mygraph,ordering,finishingtime,leader,leaderlist,1)
    #print("(mygraph,ordering,finishingtime,leader,leaderlist) \n",(mygraph,ordering,finishingtime,leader,leaderlist))
    for node in list(mygraph.nodes.keys()):        mygraph.nodes[node].explored = False
    (mygraph,ordering,finishingtime,leader,leaderlist) = dfs_pass_looper(mygraph,ordering,finishingtime,leader,leaderlist,2)
    #print("\n(mygraph,ordering,finishingtime,leader,leaderlist) \n",(mygraph,ordering,finishingtime,leader,leaderlist))
    clusters = defaultdict(list)
    for node,group in leaderlist.items():
        clusters[group].append(node)
    clusterlist = []
    for cluster in clusters.keys():
        clusterlist.append(clusters[cluster])
    return clusterlist

if __name__ == "__main__":
    #test 1
    print("test 1")
    starttime = time.time()
    g = { 1 : [2,6],
          2 : [5],
          3 : [],
          4 : [1,3],
          5 : [2,4],
          6 : [4]
        }
    for i in range(10000):
        clusters = find_strong_components_directed_graph(g)
    print(clusters)
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
    for i in range(10000):
        clusters = find_strong_components_directed_graph(g)
    print("clusters are",clusters)
    print("time taken = ",time.time()-starttime)