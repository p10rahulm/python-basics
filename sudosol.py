from math import sqrt
from itertools import combinations
import time
from queue import Queue
from collections import defaultdict
import sys

buildtime = 0
reducercstime = 0
reducenodetime = 0
rcsbuildtime = 0
nodebuildtime = 0
deepcopytime = 0
rbipartitetime =0
numsudokuobjects = 0
globaliter = 0


class Sudoku(object):
    def __init__(self, input_list):
        starttime = time.time()
        self.input_list = input_list
        self.build_matrix(self.input_list)
        self.reducedtovaluelastloop = True
        self.unsolvable = False


    def getmin_unfillednode(self):
        minnode = None
        lenmin = 10
        # print("mystr",self.get_list_as_string())
        for node in self.nodesleft:
            if node.length < lenmin:
                lenmin = node.length
                minnode = node
        return minnode

    def getOrderedMinnodesUnfilled(self):
        minnodes = []
        lenmin = 10
        for node in self.nodesleft:
            if node.length == lenmin:
                minnodes.append(node)
            elif node.length < lenmin:
                lenmin = node.length
                del minnodes[:]
        return minnodes



    def shownodeslist(self,filename=None):
        mylist = []
        for i in range(len(self.nodes)):
            mylist.append(self.nodes[i].allowedset)
        if filename is not None:
            with open(filename, 'a') as file: file.write(str(mylist))
        else: print(mylist)

    def checksolved(self):
        # print("in checksolved")
        solved = True
        for row in self.rows:
            if not row.isfixed():
                # print("row is not fixed",)
                # for elem in row: print(elem.allowedset,)
                solved = False
                break
        if solved:
            for col in self.cols:
                if not col.isfixed():
                    # print("col is not fixed",)
                    # for elem in col: print(elem.allowedset,)
                    solved = False
                    break
        if solved:
            for square in self.squares:
                if not square.isfixed():
                    # print("square is not fixed",)
                    solved = False
                    break
        self.solved = solved
        # print(self.solved)
        return self.solved

    def badresponse(self):
        # print("in checkfilled")
        if self.unsolvable: return True
        # print("in badresopnse")
        solved = True
        for elem in self.nodes:
            #print("elem = ",elem,"len(elem)=",len(elem.allowedset),"elem")
            if len(elem.allowedset) != 1:
                # print("elem.allowedset",elem.allowedset)
                solved = False
                break
        self.solved = solved
        # print(self.solved,self.nodes[2].allowedset)
        return self.solved

    def get_list(self):
        self.currentlist = []
        for node in self.nodes:
            if len(node.allowedset) == 1:
                self.currentlist.append(tuple(node.allowedset)[0])
            else:
                self.currentlist.append(None)
        return self.currentlist

    def get_list_as_string(self):
        nodevaluelist = self.get_list()
        return str(nodevaluelist)

    def runreduceLoop(self):
        while not self.unsolvable:
            if not self.reduceLoop(): return

    def reduceLoop(self):
        # self.shownodeslist("data/sudokulog.txt")
        if self.reducenodesimple(): return True
        if self.reducercssimple():return True
        if self.reducenodecomplex(): return True
        # print("returning false in reduceloop")
        # sys.exit()
        if self.reducercs():  return True # reduce rows columns and squares
        if self.reducebipartitercs():            return True
        # print("returning false in reducebipartitercs")
        # sys.exit()

        return False

    def reducenodesimple(self):
        for node in self.nodesleft:
            if node.reducesimple(): return True
        return False

    def reducercssimple(self):
        for objlist in (self.rows,self.cols,self.squares):
            for obj in objlist:
                if not obj.fixed:
                    if obj.updatercsneighbours(): return True
        return False

    def reducenodecomplex(self):
        for node in self.nodesleft:
            if node.reducecomplex(): return True
        return False

    def reducercs(self):
        for objlist in (self.rows,self.cols,self.squares):
            for obj in objlist:
                if not obj.fixed:
                    if obj.reduce_subsets(): return True
        return False
        # for row in self.rows:
        #     if not row.fixed:
        #         if row.reduce_subsets(): return True
        # for col in self.cols:
        #     if not col.fixed:
        #         if col.reduce_subsets(): return True
        # for square in self.squares:
        #     if not square.fixed:
        #         if square.reduce_subsets(): return True
        # return False

    def reducebipartitercs(self):
        reduced = False
        for row in self.rows:
            if not row.fixed:
                reduced = reduced or row.reducebipartite() #:                    return True
        for col in self.cols:
            if not col.fixed:
                reduced = reduced or col.reducebipartite() #if col.reducebipartite(): return True
        for square in self.squares:
            if not square.fixed:
                reduced = reduced or square.reducebipartite() #if square.reducebipartite(): return True
        return reduced


    def __deepcopy__(self):
        result = Sudoku(self.get_list())
        for i in range(81):
            result.nodes[i].allowedset = self.nodes[i].allowedset.copy()
            result.nodes[i].value = self.nodes[i].value
            result.nodes[i].fixed = self.nodes[i].fixed
            result.nodes[i].length = self.nodes[i].length
        for tups in ((result.rows,self.rows),(result.cols,self.cols),(result.squares,self.squares)):
            for i in range(9):
                tups[0][i].fixed = tups[1][i].fixed
                tups[0][i].numbertolocation = tups[1][i].numbertolocation.copy()

        return result

    def build_matrix(self, input_matrix):
        global buildtime
        buildtimest = time.time()
        self.rows = []
        self.cols = []
        self.squares = []
        self.nodes = []
        self.nodesleft = []
        global rcsbuildtime
        global nodebuildtime
        looptime = time.time()
        for i in range(9):
            newrow = Row(self)
            self.rows.append(newrow)
            newcol = Col(self)
            self.cols.append(newcol)
            newsq = Square(self)
            self.squares.append(newsq)
        rcsbuildtime += time.time() - looptime
        looptime = time.time()
        for i in range(81):
            looptime = time.time()
            if input_matrix[i] is not None:
                newnode = Node(self.rows[i // 9], self.cols[i % 9], self.squares[((i // 27) * 3) + ((i % 9) // 3)],self,set([input_matrix[i]]),True,input_matrix[i],1,i)
                newnode.row.unsolved -= 1
                newnode.col.unsolved -= 1
                newnode.square.unsolved -= 1
            else:
                newnode = Node(self.rows[i // 9], self.cols[i % 9], self.squares[((i // 27) * 3) + ((i % 9) // 3)],self,set(range(1,10)),False,None,9,i)
                self.nodesleft.append(newnode)
                newnode.row.nodesleft.add(newnode)
                newnode.col.nodesleft.add(newnode)
                newnode.square.nodesleft.add(newnode)
            nodebuildtime += time.time() - looptime
            self.nodes.append(newnode)
            inlooptime = time.time()
            self.rows[i // 9].append(newnode)
            self.cols[i % 9].append(newnode)
            self.squares[((i // 27) * 3) + ((i % 9) // 3)].append(newnode)
            rcsbuildtime += time.time() - inlooptime
        for i in range(9):
            self.rows[i].rcsnumtodictinitilize()
            self.cols[i].rcsnumtodictinitilize()
            self.squares[i].rcsnumtodictinitilize()

        for i in range(81):
            if input_matrix[i] is not None:
                self.rows[i//9].numbertolocation[input_matrix[i]] = set([self.nodes[i]])
                self.cols[i%9].numbertolocation[input_matrix[i]] = set([self.nodes[i]])
                self.squares[((i // 27) * 3) + ((i % 9) // 3)].numbertolocation[input_matrix[i]] = set([self.nodes[i]])
        # self.rows[0].shownldict()
        # sys.exit()
        nodebuildtime += time.time() - looptime
        buildtime += time.time() - buildtimest

    def solutiondriverNoGuess(self):
        self.runreduceLoop()
        if self.checksolved():
            return self
        elif self.badresponse():
            return "Bad Response"
        return None


class RCS(object):
    def __init__(self):
        self.nodesleft = set()
        self.fixed = False
        self.numbertolocation = defaultdict(set)

    def shownldict(self):
        g = defaultdict(list)
        for i in self.numbertolocation:
            for node in self.numbertolocation[i]:
                g[i].append(node.id)
        # print(g)
        for i in g:        print("g[",i,"]= ",g[i] )
        # for i in g: print("g[",i,"]= ",self.numbertolocation[i])
        return g

    def reversenldict(self):
        g = defaultdict(set)
        for i in self.numbertolocation:
            nodeset = self.numbertolocation[i]
            h = set()
            for node in nodeset:h.add(node.id)
            # print(nodeset)
            g[frozenset(h)].add(i)
        # print("")
        # for i in g:        print("g[",i,"]= ",g[i] )
        # sys.exit()
        return g

    def rcsnumtodictinitilize(self):
        for i in range(1,10):
            for node in self:
                self.numbertolocation[i].add(node)

    def showrcs(self):
        res = []
        for i in self: res.append(set(i.allowedset))
        return str(res)


    def isfixed(self):
        # print("in isfixed. self.unsolved",self.unsolved,"self.",self.showrcs())
        if not self.fixed:
            if self.unsolved !=0: return False
            else:
                elemset = set()
                for elem in self:
                    if len(elem.allowedset) == 1:                    elemset.add(tuple(elem.allowedset)[0])
                    else: return False
                if elemset == set(range(1, 10)):
                    self.fixed = True
                else:
                    self.fixed = False
                    self.mainsquare.unsolvable = True
        return self.fixed

    def reduce_subsets(self):
        subsetlentocheck = 1
        reduced = False
        nodesleftcopy = self.nodesleft.copy()
        while subsetlentocheck < len(self.nodesleft) and len(self.nodesleft) > 2:
            for subset in combinations(nodesleftcopy, subsetlentocheck):
                # get all possible elements in combination subset
                elemset = set([])
                subsetinvalid = False
                for node in subset:
                    if node not in self.nodesleft: subsetinvalid = subsetinvalid or True
                if subsetinvalid: continue
                for node in subset:                    elemset = elemset.union(node.allowedset)
                # if these possible elements equal length of subset, then we can eliminate those from all other unfilled elements in the row
                if len(elemset) == subsetlentocheck:
                    for notsubsetelem in self.nodesleft.difference(subset):
                        # for i in subset:print("subset.allowedset = ",i.allowedset)
                        # print("calling from reduce subsets. Subset=",subset,"elemset = ",elemset,"subsetlentocheck","notsubsetelem",notsubsetelem,"and",notsubsetelem.allowedset)
                        # print(self.showrcs())
                        # self.shownldict()
                        (reducedsizeforElem, reducedtoval) = notsubsetelem.reduceSet(elemset)
                        if reducedtoval: return True
                        reduced = reduced or reducedsizeforElem
            subsetlentocheck += 1
        return reduced

    def updatercsneighbours(self):
        # print("beforeupdatercsneighbours",self.showrcs())
        # self.shownldict()
        reduced = False
        for num in self.numbertolocation:
            if len(self.numbertolocation[num]) ==1:
                snode = tuple(self.numbertolocation[num])[0]
                # print("num",num,"self.numbertolocation[num]",self.numbertolocation[num],"snode",snode.id,"snode.allowedset",snode.allowedset)
                (reducedelem,reducedtoval) = snode.setSet(set([num]))
                # print("num",self.numbertolocation[num],"snode",snode.id,"snode.allowedset",snode.allowedset)
                # sys.exit()
                reduced = reduced or reducedelem
                for node in self.nodesleft.copy():
                    if node.id != snode.id:
                        (reducedelem,reducedtoval) = node.reduceElem(num)
                        reduced = reduced or reducedelem
        # self.shownldict()
        # print("after",self.showrcs())
        return reduced
                #
                # for num2 in self.numbertolocation:
                #     if num2 != num:
                #         self.numbertolocation[num2].discard(tuple(self.numbertolocation[num])[0])
                #         for node in self.numbertolocation[num2].copy():
                #             node.reduceElem(num)


    def reducebipartite(self):
        reduced = False
        reversedict = self.reversenldict()
        for nodeset in reversedict:
            if len(nodeset) == len(reversedict[nodeset]):
                for node in nodeset:
                    (reducednode,reducedtoval) = self.mainsquare.nodes[node].setSet(reversedict[nodeset])
                    reduced = reduced or reducednode
                # self.shownldict()
                for node in self.nodesleft:
                    if node.id not in nodeset:
                        # print("last in reduce bipartite")
                        # m = []
                        # for node1 in nodeset: m.append(node1)
                        # print("node.id = ",node.id,"set(reversedict[nodeset]) = ",set(reversedict[nodeset]),"nodeset = ",m, "node not in nodeset",node not in nodeset,
                        #       "\nnode = ",node,"\nnodeset = ",nodeset,"\nnode[45] = ",self.mainsquare.nodes[45])
                        (reducednode,reducedtoval) = node.reduceSet(reversedict[nodeset])
                        reduced = reduced or reducednode
        return reduced


        # # self.updatercsneighbours()
        # print("")
        # self.shownldict()
        # # print(self.numbertolocation[5])
        # reduced = False
        # permutationtonodedict =defaultdict(set)
        # if not self.fixed:
        #     for num in self.numbertolocation:
        #         nodesfornumset = frozenset(self.numbertolocation[num])
        #         permutationtonodedict[nodesfornumset].add(num)
        #     for nodesfornumset in permutationtonodedict:
        #         if len(nodesfornumset) == len(permutationtonodedict[nodesfornumset]) and len(nodesfornumset)>1:
        #             for node in nodesfornumset:
        #                 if not node.fixed:
        #                     (reducednode,reducedtoval) = node.setSet(permutationtonodedict[nodesfornumset].copy())
        #                     reduced = reduced or reducednode
        #             for node in  self.nodesleft.difference(nodesfornumset):
        #                 (reducednode,reducedtoval) = node.reduceSet(permutationtonodedict[nodesfornumset].copy())
        #                 reduced = reduced or reducednode
        # if reduced:
        #     self.shownldict()
        #     self.reversenldict()
        #     sys.exit()
        # return reduced


    #
    # def reducebipartite(self):
    #     global rbipartitetime
    #     starttime = time.time()
    #     reduced = False
    #     permutationtonodedict =defaultdict(set)
    #     if not self.fixed:
    #         m = defaultdict(list)
    #         # print("m=",self.numbertolocation)
    #         for num in self.numbertolocation:
    #             # print("num",num,"self.numbertolocation[num]",self.numbertolocation[num])
    #             for i in self.numbertolocation[num]:
    #                 m[num].append(i.allowedset)
    #         print("num = ",num,"self.numbertolocation[num] = ",m)
    #         global globaliter
    #         globaliter+=1
    #         # if globaliter ==8:            sys.exit()
    #         for num in self.numbertolocation:
    #             nodesfornumset = frozenset(self.numbertolocation[num])
    #             permutationtonodedict[nodesfornumset].add(num)
    #
    #         for permutation in permutationtonodedict:
    #             if len(permutation) == len(permutationtonodedict[permutation]) and len(permutation)>1:
    #                 self.iter+=1
    #                 m = []
    #                 for i in permutation: m.append(i.allowedset)
    #                 print("m = ", m,"permutationtonodedict[permutation] = ",permutationtonodedict)
    #                 sys.exit()
    #                 for node in permutation:
    #                     if not node.fixed:
    #                         (reducednode,reducedtoval) = node.setSet(permutationtonodedict[permutation].copy())
    #                         reduced = reduced or reducednode
    #                 for node in  self.nodesleft.difference(permutation):
    #                     (reducednode,reducedtoval) = node.reduceSet(permutationtonodedict[permutation].copy())
    #                     reduced = reduced or reducednode
    #     if reduced: print("reduced in reducedbipartite")
    #     return reduced


        # # print("in reducebipartite")
        # subsetlentocheck = 1
        # numstocheck = set()
        # reduced = False
        # for i in self.nodesleft:
        #     numstocheck = numstocheck.union(i.allowedset)
        #     # print("node.availableset",i.allowedset)
        # while subsetlentocheck < len(numstocheck):
        #     for subsettuple in combinations(numstocheck, subsetlentocheck):
        #         subset = set(subsettuple)
        #         elemset = set()
        #         for num in subset:
        #             elemset = elemset.union(self.numbertolocation[num])
        #         if len(elemset) == subsetlentocheck:
        #             for elem in elemset:
        #                 (reducedsizeforElem, reducedtoval) = elem.setSet(subset)
        #                 if reducedtoval:
        #                     print("reducedtoval. elemset",elemset,"elem = ",elem,"subset = ",subset)
        #                     rbipartitetime += time.time()-starttime
        #                     return True
        #                 reduced = reduced or reducedsizeforElem
        #     subsetlentocheck +=1
        # # print("returned, rresult = ", reduced)
        # rbipartitetime += time.time()-starttime
        # return reduced





class Row(list, RCS):
    def __init__(self,mainsquare):
        self.fixed = False
        self.nodesleft = set()
        self.unsolved = 9
        self.mainsquare = mainsquare
        self.numbertolocation = defaultdict(set)




class Col(list, RCS):
    def __init__(self,mainsquare):
        self.fixed = False
        self.nodesleft = set()
        self.unsolved = 9
        self.mainsquare = mainsquare
        self.numbertolocation = defaultdict(set)


class Square(list, RCS):
    def __init__(self,mainsquare):
        self.fixed = False
        self.nodesleft = set()
        self.unsolved = 9
        self.mainsquare = mainsquare
        self.numbertolocation = defaultdict(set)


class Node(object):
    def __init__(self, row, col, square,mainsquare,allowedset,fixed,value,length,id):
        self.row = row
        self.col = col
        self.square = square
        self.mainsquare = mainsquare
        self.allowedset = allowedset
        self.fixed = fixed
        self.value = value
        self.length = length
        self.id = id

    def setSet(self,setofnums):
        if self.fixed or self.length < len(setofnums): return (False,False)
        for num in range(1,10):
            if num not in setofnums:
                self.row.numbertolocation[num].discard(self)
                self.col.numbertolocation[num].discard(self)
                self.square.numbertolocation[num].discard(self)
        startlen = self.length
        self.allowedset  = setofnums.copy()
        self.length = len(self.allowedset)
        if self.length ==1:
            return self.lennowone()
        else: return (self.length < startlen,False)

    def updatercsdictvalset(self,value):
        for obj in (self.row,self.col,self.square):
            for num in range(1,10):
                if num != value:
                    obj.numbertolocation[num].discard(self)
            # self.col.numbertolocation[key].discard(self)
            # self.square.numbertolocation[key].discard(self)
            obj.numbertolocation[value] = set([self])
        # self.col.numbertolocation[value] = set([self])
        # self.square.numbertolocation[value] = set([self])




    def setValue(self,value):
        startlen = self.length
        self.updatercsdictvalset(value)
        self.allowedset = set([value])
        self.length = 1
        self.lennowone()
        # self.fixed = True
        # self.value = value
        # self.row.unsolved -=1
        # self.col.unsolved -=1
        # self.square.unsolved -=1
        # self.row.nodesleft.discard(self)
        # self.col.nodesleft.discard(self)
        # self.square.nodesleft.discard(self)
        # try:
        #     self.mainsquare.nodesleft.remove(self)
        # except ValueError:
        #     pass  # do nothing!
        # self.updateneighbours()
        # self.row.isfixed()
        # self.col.isfixed()
        # self.square.isfixed()
        return (self.length <startlen,True)


    def lennowone(self):
        self.fixed = True
        self.value = tuple(self.allowedset)[0]
        self.updatercsdictvalset(self.value)
        self.row.nodesleft.discard(self)
        self.col.nodesleft.discard(self)
        self.square.nodesleft.discard(self)
        try:
            self.mainsquare.nodesleft.remove(self)
        except ValueError:
            pass  # do nothing!
        self.updateneighbours()
        self.row.unsolved -=1
        self.row.isfixed()
        self.col.unsolved -=1
        self.col.isfixed()
        self.square.unsolved -=1
        self.square.isfixed()
        return (True, True)

    def reduceElem(self, reduceelement):
        startlen = self.length
        startfixed = self.fixed
        if not startfixed:
            for obj in (self.row,self.col,self.square):
                obj.numbertolocation[reduceelement].discard(self)
            # self.col.numbertolocation[reduceelement].discard(self)
            # self.square.numbertolocation[reduceelement].discard(self)
            #print("self.allowedset",self.allowedset,"reduceelement",reduceelement)
            self.allowedset.discard(reduceelement)#self.allowedset = self.allowedset.discard(reduceelement)
            #print("self.allowedset2",self.allowedset)
            self.length = len(self.allowedset)
            if self.length == 1:
                return self.lennowone()

        return (self.length - startlen > 0, False)

    def reduceSet(self, reduceset):
        startfixed = self.fixed
        if not startfixed:
            for obj in (self.row,self.col,self.square):
                for reduceelem in reduceset:
                    obj.numbertolocation[reduceelem].discard(self)
                    # self.col.numbertolocation[reduceelem].discard(self)
                    # self.square.numbertolocation[reduceelem].discard(self)
            startlen = self.length
            if len(self.allowedset) ==0:                print("OMGodse SERIOUS ISSUE. self.allowedset")
            newset = self.allowedset.difference(reduceset)
            if len(newset) ==0:                print("OMG SERIOUS ISSUE",self.allowedset,reduceset)
            self.allowedset = self.allowedset.difference(reduceset)
            self.length = len(self.allowedset)
            if self.length == 0:
                print("SERIOUS PROBLEM. ALLOWEDSET = ",self.allowedset,"REduceset = ",reduceset)
                # sys.exit()
                self.mainsquare.unsolvable=True
                return (True,True)
            if self.length == 1:
                return self.lennowone()
        else:
            return (False, False)
        return (self.length < startlen, False)

    def showrowlists(self):
        # print("in show row lists")
        mylist = []
        for elem in self.row:
            mylist.append(elem.allowedset)
        print("self = ", self.allowedset, "row = ", mylist)

    def showcollists(self):
        # print("in show col lists")
        mylist = []
        for elem in self.col:
            mylist.append(elem.allowedset)
        print("self = ", self.allowedset, "col = ", mylist)

    def showsqlists(self):
        # print("in show sq lists")
        mylist = []
        for elem in self.square:
            mylist.append(elem.allowedset)
        print("self = ", self.allowedset, "sq = ", mylist)


    def updateneighbours(self):
        # print("in update neigbours", )
        # self.showrowlists()
        # self.showcollists()
        # self.showsqlists()
        if not self.row.fixed:
            for elem in self.row.nodesleft.copy():
                if elem is not self and not elem.fixed:
                    elem.reduceElem(self.value)
        if not self.col.fixed:
            for elem in self.col.nodesleft.copy():
                if elem is not self and not elem.fixed:
                    elem.reduceElem(self.value)
        if not self.square.fixed:
            for elem in self.square.nodesleft.copy():
                if elem is not self and not elem.fixed:
                    elem.reduceElem(self.value)

    def reducesimple(self):
        if self.fixed: return False
        setofelems = set()
        for rcselem in self.row + self.col + self.square:
            if rcselem.fixed:
                #print("rcselem.allowedset",rcselem.allowedset,"setofelems",setofelems)
                setofelems.add(rcselem.value)
        return self.reduceSet(setofelems)[0]

    def reducecomplexgivenrcs(self,rcs):
        # print("in reduce complex, rcs = ",rcs)
        if self.fixed: return False
        for num in rcs.numbertolocation:
            if len(rcs.numbertolocation[num]) ==1:
                valset = rcs.numbertolocation[num]
                node = tuple(valset)[0]
                if node.fixed: continue
                node.setValue(num)
                # self.updateneighbours()
                return True
        return False

        # setofelems = set()
        # for rcselem in rcs:
        #     if rcselem is not self: setofelems = setofelems.union(rcselem.allowedset)
        # if len(setofelems) == 8:
        #     reductionset = set(range(1,10)).difference(setofelems)
        #     self.setValue(tuple(reductionset)[0])
        #     self.updateneighbours()
        #     return True
        # return False

    def reducecomplex(self):
        if self.fixed: return False
        if self.reducecomplexgivenrcs(self.row): return True
        # print("returning false in reducecomplex row")
        # sys.exit()
        if self.reducecomplexgivenrcs(self.col): return True
        if self.reducecomplexgivenrcs(self.square): return True
        # print("returning false in reducecomplex")
        # sys.exit()
        return False

def dfsreduceall(sudokuObject):
    response = sudokuObject.solutiondriverNoGuess()
    if response == "Bad Response":        return None
    elif type(response) is Sudoku: return response
    else:
        minnode = sudokuObject.getmin_unfillednode()
        if len(minnode.allowedset) == 0:
            return None
        permutor = set()
        for i in minnode.allowedset: permutor.add(i)
        for permuted in permutor:
            global numsudokuobjects
            numsudokuobjects += 1
            # minnode.setValue(permuted)
            global deepcopytime
            looptime = time.time()
            newsudokuObject = sudokuObject.__deepcopy__()
            newsudokuObject.nodes[minnode.id].setValue(permuted)
            deepcopytime += time.time() - looptime
            solvediteration = dfsreduceall(newsudokuObject)
            if solvediteration is not None:
                return solvediteration
        return None

def bfsreduceall(sudokuObject):

    source = sudokuObject.solutiondriverNoGuess()
    if source == "Bad Response":        return None
    elif type(source) is Sudoku: return source

    Q = Queue([sudokuObject])
    loop = 1
    startminnodes = None
    while not Q.isempty():
        # print("loop no",loop)
        if loop >2: return dfsreduceall(sudokuObject)
        # if startminnodes is not None:
        #     for node in startminnodes:print(node.allowedset,node.id)
        # print("Q.unqueue()",Q)
        v = Q.unqueue()
        unfnodes = v.getOrderedMinnodesUnfilled() #unfinished nodes
        if loop ==1:startminnodes = unfnodes
        for minnode in unfnodes:
            for permutedvalue in minnode.allowedset:
                global numsudokuobjects
                numsudokuobjects += 1
                newsudokuObject = sudokuObject.__deepcopy__()
                newsudokuObject.nodes[minnode.id].setValue(permutedvalue)
                postsolveobject = newsudokuObject.solutiondriverNoGuess()
                if type(postsolveobject) is Sudoku: return postsolveobject
                elif postsolveobject != "Bad Response": Q.enqueue(newsudokuObject)
                loop +=1

    return None



def run_sudokusolver(input_string):
    input_list = []
    sudoobj = None
    specification = 0
    for char in input_string:
        if char != '.':
            input_list.append(int(char))
            specification +=1
        else: input_list.append(None)
    print("specification of puzzle = ",specification)
    sudoobj = Sudoku(input_list)
    sudoobj = dfsreduceall(sudoobj)
    # sudoobj = bfsreduceall(sudoobj)
    if sudoobj is not None:
        solvedstring = sudoobj.get_list_as_string()
    else:
        print("FAILURE")
        # sys.exit()
        solvedstring = "Unable to solve puzzle"
    return solvedstring


if __name__ == "__main__":
    starttime = time.time()
    # numsudokuobjects = 0
    # input_string = '.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8'
    # print(run_sudokusolver(input_string))
    # print("number of sudoku objects created = ", numsudokuobjects)
    #
    # numsudokuobjects = 0
    # input_string = '29416735831548962767825349145631287998357421672169853456294178383972614514783596.'
    # print(run_sudokusolver(input_string))
    # print("number of sudoku objects created = ", numsudokuobjects)
    #
    # numsudokuobjects = 0
    # input_string = '...16...831..896..67....49.45..12..9983.7..167..698..456....78383..26145.....596.'
    # print(run_sudokusolver(input_string))
    # print("number of sudoku objects created = ", numsudokuobjects)
    #
    # numsudokuobjects = 0
    # input_string = '48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....'
    # print(run_sudokusolver(input_string))
    # print("number of sudoku objects created = ", numsudokuobjects)

    numsudokuobjects = 0
    input_string = '....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ", numsudokuobjects)

    print("time taken = ", time.time() - starttime)
    #
    # numsudokuobjects = 0
    # # starttime = time.time()
    # toughsudokufile = filename = 'data/toughsudokupuzzles.txt'
    # sudokupuzzles = []
    # with open(toughsudokufile) as inputfile:
    #     for line in inputfile:
    #         sudokupuzzles.append(line.strip())
    # puzzleno = 1
    # for puzzle in sudokupuzzles:
    #     run_sudokusolver(puzzle)
    #     # print(run_sudokusolver(puzzle))
    #     puzzleno += 1
    #     # if puzzleno ==5: break
    #
    # print("time taken = ", time.time() - starttime)
    # print("build time taken = ", buildtime)
    # print("rcs buildtime = ", rcsbuildtime)
    # print("node buildtime = ", nodebuildtime)
    # print("reduce rcs time taken = ", reducercstime)
    # print("reduce node time taken = ", reducenodetime)
    # print("deepcopytime= ", deepcopytime)
    # print("time spent inside bipartite= ", rbipartitetime)
    # print("number of sudoku objects created = ", numsudokuobjects)

