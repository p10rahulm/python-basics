from graph import Graph
from graph import Node
from collections import defaultdict
import time
from openfile import read_graph_edges_from_file
import sys
sys.setrecursionlimit(10000)
counter = 0

def dfs_pass_looper(mygraph,ordering,finishingtime,leader,leaderlist,passnumber,nedges = None):
    print("Inside DFS Pass Looper")
    if passnumber == 1:
        nodesorder  = list(mygraph.nodes.keys())[::-1]
        mygraph.reverse_graph()
        print("Got Reversed Graph")
    else:
        nodes = list(mygraph.nodes.keys())
        nodesorder = [0]*len(nodes)
        for node in nodes:
            nodesorder[ordering[node]-1] = node
        nodesorder = nodesorder[::-1]
        print("Got nodesorder for pass 2")
    print("starting the actual DFS")
    for node in nodesorder:
        if mygraph.nodes[node].explored == False:
            if passnumber == 2: leader = node
            (mygraph,ordering,finishingtime,leader,leaderlist) = dfs_DAG(mygraph,node,leader,leaderlist,ordering,finishingtime,passnumber)
    return (mygraph,ordering,finishingtime,leader,leaderlist)



def dfs_DAG(mygraph,source,leader,leaderlist,ordering,finishingtime,passnumber):
    global counter
    counter += 1
    print("DFS number", counter)

    mygraph.nodes[source].explored = True
    if passnumber == 2: leaderlist[source] = leader
    if passnumber == 1:
        iterlist = mygraph.reversedgraph[source] #[mygraph.sourcenodes[i] for i in range(len(mygraph.destnodes)) if mygraph.destnodes[i] == source]
    else:
        iterlist = mygraph.graph_dict[source]

    for secondnode in iterlist:
        print("finishingtime,leader,leaderlist,secondnode\n",finishingtime,leader,leaderlist,secondnode)
        if mygraph.nodes[secondnode].explored != True:
            print("i'm inside if for second node")
            (mygraph,ordering,finishingtime,leader,leaderlist) = dfs_DAG(mygraph,secondnode,leader,leaderlist,ordering,finishingtime,passnumber)
    print("returned dag. Node no:",finishingtime, "counter = ",counter-1)
    counter -= 1
    if passnumber ==1:
        finishingtime += 1
        ordering[source] = finishingtime
    return (mygraph,ordering,finishingtime,leader,leaderlist)


def find_strong_components_directed_graph(graph_dictionary,nedges):
    mygraph = Graph(graph_dictionary)
    print("graph built")
    size = len(mygraph.nodes)
    print("size taken")
    finishingtime = 0
    ordering = {}
    leader = None
    leaderlist = {}
    (mygraph,ordering,finishingtime,leader,leaderlist) = dfs_pass_looper(mygraph,ordering,finishingtime,leader,leaderlist,1,nedges)
    #print("(mygraph,ordering,finishingtime,leader,leaderlist) \n",(mygraph,ordering,finishingtime,leader,leaderlist))
    for node in list(mygraph.nodes.keys()):        mygraph.nodes[node].explored = False
    print("part1 done")
    (mygraph,ordering,finishingtime,leader,leaderlist) = dfs_pass_looper(mygraph,ordering,finishingtime,leader,leaderlist,2)
    print("part2 done")
    #print("\n(mygraph,ordering,finishingtime,leader,leaderlist) \n",(mygraph,ordering,finishingtime,leader,leaderlist))
    clusters = defaultdict(list)
    for node,group in leaderlist.items():
        clusters[group].append(node)
    clusterlist = []
    for cluster in clusters.keys():
        clusterlist.append(len(clusters[cluster]))

    return clusterlist.sort(reverse=True)[:10]


if __name__ == "__main__":
    '''
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

    '''
    print("we start")
    (g,nedges) = read_graph_edges_from_file("data/scc.txt")
    print("read g. nlines = ",nedges)

    clusters = find_strong_components_directed_graph(g,nedges)
    print(clusters)