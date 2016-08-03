from collections import defaultdict
import pickle

def openfile_returnlist(csvfilename):
    with open(csvfilename) as f:
        x = list(map(float, f))
    return x

def openfile_returnlist_as_string(filename):
    with open(filename) as f:
        x = list(map(str, f))
    return x


def openAdjListwithWeightsfromFile(filename):
    g = open(filename,'r')
    edges = []
    for line in g:
        x, *y = line.strip().split("\t")
        for nodetuple in y:
            nodetuple = nodetuple.split(",")
            othernode = int(nodetuple[0])
            weight = int(nodetuple[1])
            edges.append((int(x),othernode,weight))
    g.close()
    return edges

def openNumberstoDictfromFile(filename):
    dict = {}
    g = open(filename,'r')
    for line in g:
        x = int(line.strip())
        dict[x] = 1
    g.close()
    return dict

def writelisttofile(outfilepath,itemlist):
    with open(outfilepath, 'w') as file_handler:
        for item in itemlist:
            file_handler.write("{}\n".format(item))
    # outfile = open( outfilepath, "w" )
    # for item in itemlist:
    #     print>>outfile, item
    # outfile.close()

def writelisttofilepickle(outfilepath,itemlist):
    outfile = open( outfilepath, "wb" )
    pickle.dump(itemlist, outfile)
    outfile.close()


def readlistfromfilepickle(infilepath):
    infile = open( infilepath, "rb" )
    itemlist = pickle.load(infile)
    infile.close()
    return itemlist

def openNumberstoListfromFile(filename):
    mylist = []
    g = open(filename,'r')
    for line in g:
        x = int(line.strip())
        mylist.append(x)
    g.close()
    return mylist


def openAdjListfromFile(filename):
    g = open(filename,'r')
    graph = defaultdict(list)
    for line in g:
        x, *y = map(int, line.split())
        graph[x]=y
    return graph

def read_graph_edges_from_file(filename):
    g = open(filename,'r')
    graph = defaultdict(list)
    nlines =0
    for line in g:
        (x, y) = line.strip().split() #map(int, line.strip().split(" "))
        if(x==y):
            print("loops exist, x = ",x,"; y = ", y)
        else:
            graph[x].append(y)
        nlines += 1
    return graph,nlines

def adj_list_to_file(G,file_name):
    f = open(file_name, "w")
    for n in G.nodes():
        f.write(str(n) + ' ')
        for neighbor in G.neighbors(n):
            f.write(str(neighbor) + ' ')
        f.write('\n')


if __name__ == "__main__":
    #mylist = openfile_returnlist("data/CountInversionsData.txt")
    edges = openAdjListwithWeightsfromFile("data/djikstra.txt")
    print(edges[:20])

