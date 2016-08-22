from math import sqrt
from itertools import combinations
import time
import sys

buildtime = 0
reducercstime = 0
reducenodetime = 0
rcsbuildtime = 0
nodebuildtime = 0
deepcopytime = 0

numsudokuobjects = 0


class Sudoku(object):
    def __init__(self, input_list):
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
                    solved = False
                    break
        if solved:
            for square in self.squares:
                if not square.isfixed():
                    solved = False
                    break
        self.solved = solved
        # print(self.solved)
        return self.solved

    def checkfilled(self):
        # print("in checkfilled")
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
        if self.reducenodecomplex(): return True
        if self.reducercs():  # reduce rows columns and squares
            return True
        return False

    def reducenodesimple(self):
        for node in self.nodesleft:
            if node.reducesimple(): return True
        return False

    def reducenodecomplex(self):
        for node in self.nodesleft:
            if node.reducecomplex(): return True
        return False

    def reducercs(self):
        for row in self.rows:
            if not row.fixed:
                if row.reduce_subsets(): return True
        for col in self.cols:
            if not col.fixed:
                if col.reduce_subsets(): return True
        for square in self.squares:
            if not square.fixed:
                if square.reduce_subsets(): return True
        return False

    def __deepcopy__(self):
        result = Sudoku(self.get_list())
        for i in range(81):
            result.nodes[i].allowedset = self.nodes[i].allowedset.copy()
            result.nodes[i].value = self.nodes[i].value
            result.nodes[i].fixed = self.nodes[i].fixed
            result.nodes[i].length = self.nodes[i].length
        for i in range(9):
            result.rows[i].fixed = self.rows[i].fixed
            result.cols[i].fixed = self.cols[i].fixed
            result.squares[i].fixed = self.squares[i].fixed

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
                newnode = Node(self.rows[i // 9], self.cols[i % 9], self.squares[((i // 27) * 3) + ((i % 9) // 3)],self,set([input_matrix[i]]),True,input_matrix[i],1)
                newnode.row.unsolved -= 1
                newnode.col.unsolved -= 1
                newnode.square.unsolved -= 1
            else:
                newnode = Node(self.rows[i // 9], self.cols[i % 9], self.squares[((i // 27) * 3) + ((i % 9) // 3)],self,set(range(1,10)),False,None,9)
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
        nodebuildtime += time.time() - looptime
        buildtime += time.time() - buildtimest


class RCS(object):
    def __init__(self):
        self.nodesleft = set()
        self.fixed = False

    def isfixed(self):
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
                for node in subset:                    elemset = elemset.union(node.allowedset)
                # if these possible elements equal length of subset, then we can eliminate those from all other unfilled elements in the row
                if len(elemset) == subsetlentocheck:
                    for notsubsetelem in self.nodesleft.difference(subset):
                        #for i in subset:print("subset.allowedset = ",i.allowedset)
                        #print("calling from reduce subsets. Subset=",subset,"elemset = ",elemset,"subsetlentocheck","notsubsetelem",notsubsetelem,"and",notsubsetelem.allowedset)
                        (reducedsizeforElem, reducedtoval) = notsubsetelem.reduceSet(elemset)
                        if reducedtoval: return True
                        reduced = reduced or reducedsizeforElem
            subsetlentocheck += 1
        return reduced


class Row(list, RCS):
    def __init__(self,mainsquare):
        self.fixed = False
        self.nodesleft = set()
        self.unsolved = 9
        self.mainsquare = mainsquare


class Col(list, RCS):
    def __init__(self,mainsquare):
        self.fixed = False
        self.nodesleft = set()
        self.unsolved = 9
        self.mainsquare = mainsquare


class Square(list, RCS):
    def __init__(self,mainsquare):
        self.fixed = False
        self.nodesleft = set()
        self.unsolved = 9
        self.mainsquare = mainsquare


class Node(object):
    def __init__(self, row, col, square,mainsquare,allowedset,fixed,value,length):
        self.row = row
        self.col = col
        self.square = square
        self.mainsquare = mainsquare
        self.allowedset = allowedset
        self.fixed = fixed
        self.value = value
        self.length = length


    def setValue(self,value):
        startfixed = self.fixed
        if startfixed:
            self.allowedset = set([value])
            self.value = value
        else:
            self.allowedset = set([value])
            self.length = 1
            self.fixed = True
            self.value = value
            self.row.unsolved -=1
            self.col.unsolved -=1
            self.square.unsolved -=1
        self.row.nodesleft.discard(self)
        self.col.nodesleft.discard(self)
        self.square.nodesleft.discard(self)
        try:
            self.mainsquare.nodesleft.remove(self)
        except ValueError:
            pass  # do nothing!
        #self.updateneighbours()
        self.row.isfixed()
        self.col.isfixed()
        self.square.isfixed()

    def reduceElem(self, reduceelement):
        startlen = self.length
        startfixed = self.fixed
        if not startfixed:
            #print("self.allowedset",self.allowedset,"reduceelement",reduceelement)
            self.allowedset.discard(reduceelement)#self.allowedset = self.allowedset.discard(reduceelement)
            #print("self.allowedset2",self.allowedset)
            self.length = len(self.allowedset)
            # if self.length == 0:
            #     print("ELEMENT SERIOUS PROBLEM. ALLOWEDSET = ",self.allowedset,"REduceset = ",reduceelement)
            #     sys.exit()
            if self.length == 1:
                self.fixed = True
                self.value = tuple(self.allowedset)[0]
                self.row.nodesleft.discard(self)
                self.col.nodesleft.discard(self)
                self.square.nodesleft.discard(self)
                self.mainsquare.nodesleft.remove(self)
                self.updateneighbours()
                self.row.unsolved -=1
                self.row.isfixed()
                self.col.unsolved -=1
                self.col.isfixed()
                self.square.unsolved -=1
                self.square.isfixed()
                return (True, True)
        return (self.length - startlen > 0, False)

    def reduceSet(self, reduceset):
        startfixed = self.fixed
        if not startfixed:
            startlen = self.length
            # if len(self.allowedset) ==0:                print("OMGodse SERIOUS ISSUE. self.allowedset")
            newset = self.allowedset.difference(reduceset)
            # if len(newset) ==0:                print("OMG SERIOUS ISSUE",self.allowedset,reduceset)
            self.allowedset = self.allowedset.difference(reduceset)
            self.length = len(self.allowedset)
            if self.length == 0:
                # print("SERIOUS PROBLEM. ALLOWEDSET = ",self.allowedset,"REduceset = ",reduceset)
                self.mainsquare.unsolvable=True
            if self.length == 1:
                self.fixed = True
                self.value = tuple(self.allowedset)[0]
                self.row.nodesleft.discard(self)
                self.col.nodesleft.discard(self)
                self.square.nodesleft.discard(self)
                self.mainsquare.nodesleft.remove(self)
                self.updateneighbours()
                self.row.unsolved -=1
                self.row.isfixed()
                self.col.unsolved -=1
                self.col.isfixed()
                self.square.unsolved -=1
                self.square.isfixed()
                return (True, True)
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

    def reducecomplex(self):
        if self.fixed: return False
        setofelems = set()
        for rcselem in self.row:
            if rcselem is not self: setofelems = setofelems.union(rcselem.allowedset)
        if len(setofelems) == 8:
            reductionset = set(range(1,10)).difference(setofelems)
            self.setValue(tuple(reductionset)[0])
            self.updateneighbours()
            return True
        else: (reducedforrow,reducedtoval) = (False,False)
        setofelems = set()
        for rcselem in self.row:
            if rcselem is not self: setofelems = setofelems.union(rcselem.allowedset)
        if len(setofelems) == 8:
            reductionset = set(range(1,10)).difference(setofelems)
            self.setValue(tuple(reductionset)[0])
            self.updateneighbours()
            return True
        else: (reducedforcol,reducedtoval) = (False,False)
        setofelems = set()
        for rcselem in self.row:
            if rcselem is not self: setofelems = setofelems.union(rcselem.allowedset)
        if len(setofelems) == 8:
            reductionset = set(range(1,10)).difference(setofelems)
            self.setValue(tuple(reductionset)[0])
            self.updateneighbours()
            return True
        else: (reducedforsquare,reducedtoval) = (False,False)
        return reducedforrow or reducedforcol or reducedforsquare or reducedtoval

def reduceall(sudokuObject):
    reducedsomething = True
    looptime = time.time()
    sudokuObject.runreduceLoop()
    global reducenodetime
    reducenodetime += time.time() - looptime
    # print("inside reduceall")
    # while reducedsomething:
    #     #print("running reduce loop")
    #     reducedsomething = sudokuObject.run_reduce_loop()
    # print("out of while")
    if sudokuObject.checksolved():
        return sudokuObject
    elif sudokuObject.checkfilled():
        # print("inside checkfilled",sudokuObject.get_list_as_string())
        return None
    else:
        # print("in blank")
        # sudokuObject.shownodeslist()
        # for i in range(len(sudokuObject.nodes)):
        #     if len(sudokuObject.nodes[i].allowedset) == 0:
        #         # print("sudokuObject.nodes[i].allowedset",sudokuObject.nodes[i].allowedset,"i = ",i)
        #         # print("sudokuObject.get_list_as_string() =",sudokuObject.get_list_as_string())
        #         return None

        # print("inside random")
        # sudokuObject.shownodeslist()
        minnode = sudokuObject.getmin_unfillednode()
        # minnode.showrowlists()
        # minnode.showcollists()
        # minnode.showsqlists()
        # print("minnode.allowedset",minnode.allowedset)
        if len(minnode.allowedset) == 0:
            return None
        permutor = set()
        for i in minnode.allowedset: permutor.add(i)
        for permuted in permutor:
            # print("in permuted part",minnode,"permuted = ",permuted)
            global numsudokuobjects
            numsudokuobjects += 1
            # print(minnode.allowedset)
            minnode.setValue(permuted)
            # print("after setvalue")
            # print("minnode.allowedset",minnode.allowedset)
            global deepcopytime
            looptime = time.time()
            newsudokuObject = sudokuObject.__deepcopy__()
            deepcopytime += time.time() - looptime
            solvediteration = reduceall(newsudokuObject)
            if solvediteration is not None:
                # print("returning solved iteration")
                return solvediteration
        return None


def run_sudokusolver(input_string):
    input_list = []
    sudoobj = None
    for char in input_string:
        input_list.append(int(char)) if char != '.' else input_list.append(None)
    sudoobj = Sudoku(input_list)
    sudoobj = reduceall(sudoobj)
    if sudoobj is not None:
        solvedstring = sudoobj.get_list_as_string()
    else:
        print("FAILURE")
        solvedstring = "Unable to solve puzzle"
    return solvedstring


if __name__ == "__main__":
    global numsudokuobjects


    starttime = time.time()
    numsudokuobjects = 0
    input_string = '.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ", numsudokuobjects)

    numsudokuobjects = 0
    input_string = '294167358315489627678253491456312879983574216721698534562941783839726145147835962'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ", numsudokuobjects)

    numsudokuobjects = 0
    input_string = '...16...831..896..67....49.45..12..9983.7..167..698..456....78383..26145.....596.'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ", numsudokuobjects)

    numsudokuobjects = 0
    input_string = '48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ", numsudokuobjects)

    numsudokuobjects = 0
    input_string = '....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ", numsudokuobjects)

    print("time taken = ", time.time() - starttime)

    numsudokuobjects = 0
    # starttime = time.time()
    toughsudokufile = filename = 'data/toughsudokupuzzles.txt'
    sudokupuzzles = []
    with open(toughsudokufile) as inputfile:
        for line in inputfile:
            sudokupuzzles.append(line.strip())
    puzzleno = 1
    for puzzle in sudokupuzzles:
        run_sudokusolver(puzzle)
        # print(run_sudokusolver(puzzle))
        puzzleno += 1
        # if puzzleno ==6: break

    print("time taken = ", time.time() - starttime)
    print("build time taken = ", buildtime)
    print("rcs buildtime = ", rcsbuildtime)
    print("node buildtime = ", nodebuildtime)
    print("reduce rcs time taken = ", reducercstime)
    print("reduce node time taken = ", reducenodetime)
    print("deepcopytime= ", deepcopytime)
    print("number of sudoku objects created = ", numsudokuobjects)

