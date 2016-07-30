# Initialize Undirected Graph Class
from random import randint
#import time
#timestart = time.time()
#buildtime = 0
#randomedgetime = 0
#collapseedgestime = 0
#removeselfloopstime = 0
#edgechecktime = 0
#vertexsplitime = 0
#mutualvertexremovaltime = 0
#dictv2copytime = 0
#vertex2connectedstime = 0
#vertex2deletiontime= 0
#bidirectionaltime = 0
#v2conn1stpart = 0
#v2conn2ndpart = 0

class GraphBidirect(object):
    def __init__(self,graph_dict = None,bidirected = True):
        # initializes a graph object. If no dictionary or None is given, an empty dictionary will be used
        #global buildtime
        #global bidirectionaltime
        #looptime = time.time()
        #if graph_dict == None:            graph_dict = {}
        self.bidirected = bidirected
        if bidirected == False: self.graph_dict = graph_dict
        if bidirected == True:
            self.graph_dict = graph_dict
            #loopinlooptime = time.time()
            self.bidirectional()
            #bidirectionaltime += time.time() - loopinlooptime
        #print("time taken to build = ",time.time() -looptime)
        #buildtime += time.time() - looptime


    def vertices(self):
        # returns the vertices of a graph
        return list(self.graph_dict.keys())

    def edges(self):
        # returns the edges of a graph
        return self.generate_edges()

    def non_loop_edges(self):
        # returns the edges of a graph
        edger = self.generate_edges()
        for edge in edger:
            if len(edge) == 1:
                edger.remove(edge)
        return edger

    def generate_edges(self):
        # A static method generating the edges of the graph "graph". Edges are represented as sets
        # with one (a loop back to the vertex) or two vertices
        edges = []
        for vertex in self.graph_dict:
            for neighbour in self.graph_dict[vertex]:
                if vertex != neighbour:
                    edges.append({vertex, neighbour})
        return edges

    def generate_edges_without_repeat(self):
        # A static method generating the edges of the graph "graph". Edges are represented as sets
        # with one (a loop back to the vertex) or two vertices
        edges = []
        for vertex in self.graph_dict:
            for neighbour in self.graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.generate_edges():
            res += str(edge) + " "
        return res

    def add_vertex(self, vertex):
        # If the vertex "vertex" is not in self.graph_dict, a key "vertex" with an empty
        #  list as a value is added to the dictionary. Otherwise nothing has to be done.
        if vertex not in self.graph_dict:
            self.graph_dict[vertex] = []

    def add_edge(self, edge):
        # assumes that edge is of type set, tuple or list; between two vertices can be multiple edges!
        edge = set(edge)
        nodes = self.graph_dict.keys()
        if len(edge) == 2:
            (vertex1, vertex2) = tuple(edge)
            if vertex1 in nodes:
                self.graph_dict[vertex1].append(vertex2)
            else:
                self.graph_dict[vertex1] = [vertex2]
            if self.bidirected:
                if vertex2 in nodes:
                    self.graph_dict[vertex2].append(vertex1)
                else:
                    self.graph_dict[vertex2] = [vertex1]
        elif len(edge)==1:
            for insideedge in edge:
                vertex1 = insideedge
            if vertex1 in nodes:
                self.graph_dict[vertex1].append(vertex1)
            else:
                self.graph_dict[vertex1] = [vertex1]

    def bidirectional(self):
        edges = self.edges()
        edges = set(frozenset(i)for i in edges)
        self.graph_dict = {}
        for edge in edges:
            self.add_edge(edge)
        return

    def collapse_edge(self,edge,vertices):
        # assumes that edge is of type set, tuple or list; between two vertices can be multiple edges!
        #global edgechecktime
        #global vertexsplitime
        #global mutualvertexremovaltime
        #global dictv2copytime
        #global vertex2connectedstime
        #global vertex2deletiontime
        #global v2conn1stpart
        #global v2conn2ndpart
        #looptime = time.time()
        if edge == None:
            del self.graph_dict[list(self.graph_dict.keys())[0]]
            return
        #edgechecktime += time.time()-looptime
        #if edge not in self.edges(): return "Cannot remove - edge  doesn't already exist"
        #edge = set(edge)
        #looptime = time.time()
        (vertex1, vertex2) = edge
        #vertexsplitime += time.time() - looptime
        # (vertex1, vertex2) = tuple(edge)
        #looptime = time.time()
        self.graph_dict[vertex1].remove(vertex2)
        self.graph_dict[vertex2].remove(vertex1)
        #mutualvertexremovaltime += time.time() - looptime
        #looptime = time.time()
        vertex2connecteds = self.graph_dict[vertex2].copy()
        #dictv2copytime += time.time() - looptime
        #looptime = time.time()
        #loopinloop = time.time()
        for vertex2connected in vertex2connecteds:
            if vertex2connected != vertex2:
                self.graph_dict[vertex1].append(vertex2connected)
        #v2conn1stpart += time.time()-loopinloop
        #loopinloop = time.time()
        for vertex2connected in vertex2connecteds:
            if vertex2connected != vertex2:
                self.graph_dict[vertex2connected].append(vertex1)
                self.graph_dict[vertex2connected].remove(vertex2)
        #v2conn2ndpart += time.time()-loopinloop
        #vertex2connectedstime += time.time() - looptime
        #looptime = time.time()
        del self.graph_dict[vertex2]
        #vertex2deletiontime += time.time() - looptime
        return

    def remove_self_loops(self):
        dict = self.graph_dict
        nodes = list(dict.keys())
        for node in nodes:
            for secondnode in dict[node]:
                if secondnode == node:
                    self.graph_dict[node].remove(node)
        return

    def getrandomedge(self):
        dict = self.graph_dict
        nodes = list(dict.keys())
        while True:
            randomnode = nodes[randint(0,len(nodes)-1)] # newline
            randomnodelist = dict[randomnode]
            if len(randomnodelist) != 0:
                secondvertex = randomnodelist[randint(0,len(randomnodelist)-1)]
                if secondvertex != randomnode:
                    return {randomnode,secondvertex}
                    break
        return
def getmincut_randomcontraction(graphdictionary):
    #print(graphdictionary)
    graphic = GraphBidirect(graphdictionary,True)
    #print(graphic.graph_dict)
    dict_keys = list(graphic.graph_dict.keys())
    graphic.remove_self_loops()
    #global randomedgetime
    #global collapseedgestime
    #global removeselfloopstime

    while len(dict_keys) > 2:
        #loopstart = time.time()
        randedge = graphic.getrandomedge()
        #randomedgetime += time.time() - loopstart
        #print("Got random Edge : time taken to get: ", (time.time()-loopstart)*1000)
        #loopstart = time.time()
        graphic.collapse_edge(randedge,dict_keys)
        #collapseedgestime += time.time() - loopstart
        #print("Collapsed Edge : time taken to get: ", (time.time()-loopstart)*1000)
        #loopstart = time.time()
        #graphic.remove_self_loops() # not required i think as we are not adding self loops in the first place
        #removeselfloopstime += time.time() - loopstart
        #print("Removed Self Loops again : time taken to get: ", (time.time()-loopstart)*1000)
        dict_keys = list(graphic.graph_dict.keys())
        #print("Loop complete: time taken so far: ", time.time()-timestart)
    return graphic

def mincut_graph(graphdictionary):
    mygraph = getmincut_randomcontraction(graphdictionary)
    return len(mygraph.graph_dict[mygraph.vertices()[0]])

# test ----------
print("test1")
g = { "a" : ["d"],
  "b" : ["c"],
  "c" : ["b", "c", "d", "e"],
  "d" : ["a", "c"],
  "e" : ["c"],
  "f" : []
}
noedge = True
for i in range(10):
    if mincut_graph(g)!=0: noedge = False
#    print("edges = ",mincut_graph(g))
print(noedge)

#Test2
print("test2")
minsofar =0
setsofar = False
for i in range(100000):
    g = { "a" : ["b","c","d"],
      "b" : ["a","d","c"],
      "c" : ["b", "a", "d", "e","f"],
      "d" : ["b", "a", "c", "e","f"],
      "e" : ["c","d"],
      "f" : ["c","d"]
    }
    minthistime  = mincut_graph(g)
    if minsofar > minthistime or setsofar == False:
        setsofar = True
        minsofar = minthistime
print("mincut = ",minsofar)


#test3
print("test3")
from openfile import read_adj_list_from_file
graph = read_adj_list_from_file("data/karger_cut.txt")
#print("mincut = ",mincut_graph(graph))
minsofar = 100
totaltries = 100
for i in range(totaltries):
    #timestart = time.time()
    graph = read_adj_list_from_file("data/karger_cut.txt")
    g = graph
    minthistime  = mincut_graph(g)
    if minsofar > minthistime :
        setsofar = True
        minsofar = minthistime
    #print("loop number",i,"mincut = ",minsofar)
    #print("time taken in this loop",time.time()-timestart)
print("mincut = ",minsofar)
'''
print("total time taken for getting random edges : ",randomedgetime)
print("total time taken for collapse edges: ",collapseedgestime)
print("total time taken for remove self loops: ",removeselfloopstime)
print("total build time taken : ",buildtime)
print("total time taken within build for bidirectional : ",bidirectionaltime)
print("total edge check time taken : ",edgechecktime)
print("total vertex split time taken : ",vertexsplitime )
print("total mutual vertex removal time taken : ",mutualvertexremovaltime)
print("total time taken to deep copy dictionary[vertex2] : ",dictv2copytime)
print("total time taken to run vertex 2 loops : ",vertex2connectedstime )
print("total time taken to run vertex 2 subpart1 : ",v2conn1stpart )
print("total time taken to run vertex 2 subpart2 : ",v2conn2ndpart )
print("total vertex2 deletion time taken : ",vertex2deletiontime)
'''