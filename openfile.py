def openfile_returnlist(csvfilename):
    with open(csvfilename) as f:
        x = list(map(float, f))
    return x
def openfile_returnlist_as_string(csvfilename):
    with open(csvfilename) as f:
        x = list(map(str, f))
    return x

from collections import defaultdict
def read_adj_list_from_file(filename):
    g = open(filename,'r')
    graph = defaultdict(list)
    for line in g:
        x, *y = map(int, line.split())
        graph[x]=y
    return graph

from collections import defaultdict
def read_graph_edges_from_file(filename):
    g = open(filename,'r')
    graph = defaultdict(list)
    nlines =0
    for line in g:
        (x, y) = map(int, line.split())
        graph[x].append(y)
        nlines += 1
    return graph,nlines

mylist = openfile_returnlist("data/CountInversionsData.txt")
def adj_list_to_file(G,file_name):
    f = open('tst.txt', "w")
    for n in G.nodes():
        f.write(str(n) + ' ')
        for neighbor in G.neighbors(n):
            f.write(str(neighbor) + ' ')
        f.write('\n')
