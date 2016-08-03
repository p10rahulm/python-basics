# Initialize Undirected Graph Class
from random import randint
import time
timestart = time.time()

class GraphBidirect(object):
    def __init__(self,graph_dict = None,bidirected = False):
        # initializes a graph object. If no dictionary or None is given, an empty dictionary will be used
        timestart = time.time()
        global timestart
        if graph_dict == None:
            graph_dict = {}
        self.bidirected = bidirected
        if bidirected == False: self.graph_dict = graph_dict
        if bidirected == True:
            self.graph_dict = graph_dict
            self.bidirectional()
        #print("time taken to build = ",time.time() -timestart)


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
        if len(edge) == 2:
            (vertex1, vertex2) = tuple(edge)
            if vertex1 in self.graph_dict.keys():
                self.graph_dict[vertex1].append(vertex2)
            else:
                self.graph_dict[vertex1] = [vertex2]
            if self.bidirected:
                if vertex2 in self.graph_dict.keys():
                    self.graph_dict[vertex2].append(vertex1)
                else:
                    self.graph_dict[vertex2] = [vertex1]
        elif len(edge)==1:
            for insideedge in edge:
                vertex1 = insideedge
            if vertex1 in self.graph_dict.keys():
                self.graph_dict[vertex1].append(vertex1)
            else:
                self.graph_dict[vertex1] = [vertex1]

    def bidirectional(self):
        for key in self.graph_dict:
            for val in self.graph_dict[key]:
                if (val in list(self.graph_dict.keys())) and (key not in self.graph_dict[val]):
                    self.graph_dict[val].append(key)
                elif val not in list(self.graph_dict.keys()):
                    self.graph_dict[val] = [key]
        return

    def collapse_edge(self,edge,vertices):
        # assumes that edge is of type set, tuple or list; between two vertices can be multiple edges!
        if edge == None: del self.graph_dict[list(self.graph_dict.keys())[0]]
        #if edge not in self.edges(): return "Cannot remove - edge  doesn't already exist"
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        self.graph_dict[vertex1].remove(vertex2)
        self.graph_dict[vertex2].remove(vertex1)
        vertex2connecteds = self.graph_dict[vertex2].copy()
        for vertex2connected in vertex2connecteds:
            if vertex2connected != vertex2:
                self.graph_dict[vertex1].append(vertex2connected)
                self.graph_dict[vertex2connected].append(vertex1)
                self.graph_dict[vertex2connected].remove(vertex2)
        del self.graph_dict[vertex2]
        return

    def remove_self_loops(self,vertex=None):
        if vertex == None:
            for key in self.graph_dict:
                for val in self.graph_dict[key]:
                    if val == key:
                        self.graph_dict[key].remove(val)

        else:
            for val in self.graph_dict[vertex]:
                if val == vertex:
                    self.graph_dict[vertex].remove(val)

    def getrandomedge(self):
        yedges = self.edges()
        length = len(yedges)
        if  length == 0: return None
        p = randint(0,length-1)
        return yedges[p]

def getmincut_randomcontraction(graphdictionary):
    graphic = GraphBidirect(graphdictionary,True)
    dict_keys = list(graphic.graph_dict.keys())
    graphic.remove_self_loops()
    while len(dict_keys) > 2:
        #loopstart = time.time()
        randedge = graphic.getrandomedge()
        #print("Got random edge: time taken to get: ", time.time()-loopstart)
        graphic.collapse_edge(randedge,dict_keys)
        #print("Collapsed Edge : time taken to get: ", time.time()-loopstart)
        graphic.remove_self_loops()
        #print("Removed Self Loops again : time taken to get: ", time.time()-loopstart)
        dict_keys = list(graphic.graph_dict.keys())
        #print("Loop complete: time taken so far: ", time.time()-timestart)
    return graphic

def mincut_graph(graphdictionary):
    mygraph = getmincut_randomcontraction(graphdictionary)
    graphdict = mygraph.graph_dict
    for node in graphdict.keys():
        return len(graphdict[node])
    return 0


if __name__ == "__main__":
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
    for i in range(10):
        g = { "a" : ["b","c","d"],
          "b" : ["a","d","c"],
          "c" : ["b", "a", "d", "e","f"],
          "d" : ["b", "a", "d", "e","f"],
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
    from openfile import openAdjListfromFile
    graph = openAdjListfromFile("data/karger_cut.txt")
    #print("mincut = ",mincut_graph(graph))
    setsofar = False
    minsofar = 100
    for i in range(10000):
        graph = openAdjListfromFile("data/karger_cut.txt")
        g = graph
        minthistime  = mincut_graph(g)
        if minsofar > minthistime or setsofar == False:
            setsofar = True
            minsofar = minthistime
        print("loop number",i,"mincut = ",minsofar)
