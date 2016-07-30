from random import randint
import time
import numpy as np

class Node(object):
    def __init__(self,id = None,value = None,explored = False,prev =None, next = None,layer = None):
        self.id = id
        self.prev = prev
        self.next = next
        #add any more attributes you want
        self.value = value
        self.explored = explored
        self.layer = layer
        self.group = None
        self.topologicalorder = None
    def __str__(self):
        return self.id

class Graph(object):
    def __init__(self,graph_dict = None):
        if graph_dict == None:            graph_dict = {}
        self.graph_dict = graph_dict
        self.sourcenodes = np.zeros(len(list(self.graph_dict.keys()))**2,dtype = np.int) # can be other type as per preference
        self.destnodes = np.zeros(len(list(self.graph_dict.keys()))**2,dtype = np.int)
        self.edgesnumber = 0
        self.nodesnumber = 0
        self.nodes = {}
        #self.getsource_dest_nodes()
        self.createnodes()

    def createnodes(self):
        nodeholders = self.get_nodes()
        for node in (nodeholders):
            self.nodes[node] = Node(node)



    def get_edges(self):
        s = []
        for i in range(0,self.edgesnumber):
            if(self.sourcenodes[i]!=0):
                s.append((self.sourcenodes[i],self.destnodes[i]))
        return s

    def edges(self):
        return self.get_edges()

    def get_nodes(self):
        nodeslist = list(self.graph_dict.keys())
        self.nodesnumber = len(nodeslist)
        return nodeslist

    def nodes(self):
        return self.get_nodes()

    def add_node(self,node):
        self.graph_dict[node] =[]
        self.nodesnumber +=1

    def add_edge(self,edge):
        if type(edge) is not set: print("Please input edge as type set")
        (sourcenode,destnode) = tuple(edge)
        self.edgesnumber +=1
        self.sourcenodes[self.edgesnumber] = sourcenode
        self.destnodes[self.edgesnumber] = destnode
        if sourcenode in self.nodes():
            self.graph_dict[sourcenode].append(destnode)
        else: self.graph_dict[sourcenode] = [destnode]

    def getsource_dest_nodes(self):
        dict = self.graph_dict
        nodes = self.nodes()
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
        self.sourcenodes[bothzeros] =0              #remove self loops
        self.destnodes[dfrom] = collapsetonode
        self.destnodes[bothzeros] =0                #remove self loops
        self.nodesnumber -=1
        return
    def remove_self_loops(self):
        g = np.equal(self.sourcenodes,self.destnodes)
        self.sourcenodes[g]=0
        self.destnodes[g]=0
        return

    def getrandomedge(self):
        if len(self.sourcenodes) ==0: return None
        while True:
            p = randint(0,self.edgesnumber)
            if self.sourcenodes[p] !=0:
                return (self.sourcenodes[p],self.destnodes[p])

    def __str__(self):
        res = "vertices: "
        for k in self.graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.get_edges():
            res += str(edge) + " "
        return res
