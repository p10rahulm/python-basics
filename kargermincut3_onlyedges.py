from random import randint
import time
import numpy as np


randedgetime = 0
colledgetime = 0
removeselfloopstime = 0
settingtime = 0
setgtime = 0
numberofedgestime =0
setnansinsrcdestnodestime =0
class Graph(object):
    def __init__(self,graph_dict = None):
        # initializes a graph object. If no dictionary or None is given, an empty dictionary will be used
        if graph_dict == None:            graph_dict = {}
        self.graph_dict = graph_dict
        self.sourcenodes = np.zeros(len(list(self.graph_dict.keys()))**2,dtype = np.int)
        self.destnodes = np.zeros(len(list(self.graph_dict.keys()))**2,dtype = np.int)
        self.edgesnumber = 0
        self.nodesnumber = 0
        self.getsource_dest_nodes()

    def getsource_dest_nodes(self):
        dict = self.graph_dict
        nodes = list(self.graph_dict.keys())
        self.nodesnumber = len(nodes)
        i = 0
        for node in nodes:
            for secondnode in dict[node]:
                self.sourcenodes[i] = node
                self.destnodes[i] = secondnode
                self.edgesnumber +=1
                i +=1
    def collapse_edge(self,edge):
        (collapsetonode,collapsefromnode) = edge
        sfrom = np.equal(self.sourcenodes,collapsefromnode)
        sto = np.equal(self.sourcenodes,collapsetonode)
        dfrom = np.equal(self.destnodes,collapsefromnode)
        dto = np.equal(self.destnodes,collapsetonode)
        bothzeros = (sfrom * dto) + (dfrom * sto)
        self.sourcenodes[sfrom] = collapsetonode
        self.sourcenodes[bothzeros] =0
        self.destnodes[dfrom] = collapsetonode
        self.destnodes[bothzeros] =0
        self.nodesnumber -=1
        return
    def remove_self_loops(self):
        #global setgtime
        #global numberofedgestime
        #global setnansinsrcdestnodestime
        #looptime = time.time()
        g = np.equal(self.sourcenodes,self.destnodes)
        #setgtime += time.time() - looptime
        #looptime = time.time()
        self.sourcenodes[g]=0
        self.destnodes[g]=0
        #setnansinsrcdestnodestime += time.time() - looptime
        return

    def getrandomedge(self):
        if len(self.sourcenodes) ==0: return None
        while True:
            p = randint(0,self.edgesnumber)
            if self.sourcenodes[p] !=0:
                #if self.sourcenodes[p] != self.destnodes[p]:
                return (self.sourcenodes[p],self.destnodes[p])



def runkarger(graph):
    global randedgetime
    global colledgetime
    global removeselfloopstime
    global settingtime
    mygraph = Graph(graph)
    mygraph.remove_self_loops()
    while mygraph.nodesnumber > 2:
        #looptime = time.time()
        edge = mygraph.getrandomedge()
        #randedgetime += time.time() - looptime
        #looptime = time.time()
        mygraph.collapse_edge(edge)
        #colledgetime += time.time() - looptime
        #looptime = time.time()
        #mygraph.remove_self_loops()
        #removeselfloopstime += time.time() - looptime
        #looptime = time.time()
        #settingtime += time.time() - looptime
    return len(mygraph.sourcenodes[mygraph.sourcenodes!=0])/2


#test 1
testtime = time.time()
g = { 1 : [4],
  2 : [3],
  3 : [2,3,4,5],
  4 : [1,3],
  5 : [3],
  6 : []
}
minsofar =100
for i in range(10000):
    p = runkarger(g)
    if p<minsofar: minsofar = p
print("mincut is ",minsofar )
print("done test 1 in ",time.time() - testtime, "seconds")

#test2
#Test2
print("test2")
testtime = time.time()
minsofar =100
for i in range(10000):
    g = { 1 : [2,3,4],
      2 : [1,3,4],
      3 : [1,2,4,5,6],
      4 : [1,2,3, 5,6],
      5 : [3,4],
      6 : [3,4]
    }
    minthistime  = runkarger(g)
    if minsofar > minthistime:
        minsofar = minthistime
print("mincut = ",minsofar)
print("done test 2 in ",time.time() - testtime, "seconds")


#test3
print("test3")
testtime = time.time()
from openfile import read_adj_list_from_file

minsofar = 100
totaltries = 10000
readgraph = read_adj_list_from_file("data/karger_cut.txt")

for i in range(totaltries):
    minthistime  = runkarger(readgraph)
    if minsofar > minthistime :
        minsofar = minthistime
print("mincut = ",minsofar)
print("done test 3 in ",time.time() - testtime, "seconds")

print("total time taken for getting random edges : ",randedgetime)
print("total time taken for collapse edges: ",colledgetime)
print("total time taken for remove self loops: ",removeselfloopstime)
print("total time taken for setting equality of source dest nodes: ",setgtime)
print("total time taken for changing total edges in removal: ",numberofedgestime)
print("total time taken for setting nans in source dest nodes: ",setnansinsrcdestnodestime)
print("total time taken for creating sets: ",settingtime)