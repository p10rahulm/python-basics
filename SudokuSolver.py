from math import sqrt
from itertools import combinations
import time
buildtime = 0
reducercstime = 0
reducenodetime = 0
rcsbuildtime = 0
nodebuildtime = 0

numsudokuobjects = 0

class Sudoku(object):
    def __init__(self, input_list):
        self.input_list = input_list
        #sidelength = int(sqrt(len(input_list)))
        #self.input_matrix = [[input_list[k * sidelength + j] for j in range(sidelength)] for k in range(sidelength)]
        self.build_matrix(self.input_list)
        self.solved = False
        #self.checksolved()
        self.reducedtovaluelastloop = True

    def getmin_unfillednode(self):
        minnode = None
        lenmin = 9
        for node in self.nodes:
            if len(node.allowed_set)!=1 and len(node.allowed_set)<lenmin:
                lenmin=len(node.allowed_set)
                minnode = node
        return minnode

    def shownodeslist(self):
        mylist = []
        for i in range(len(self.nodes)):
            mylist.append(self.nodes[i].allowed_set)
        print(mylist)

    def checksolved(self):
        solved = True
        for row in self.rows:
            if not row.isfixed():
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
        #print(self.solved)
        return self.solved

    def checkfilled(self):
        #print("in checkfilled")
        solved = True
        for elem in self.nodes:
            if not elem.fixed:
                solved = False
                break
        self.solved = solved
        #print(self.solved)
        return self.solved

    def get_list(self):
        self.currentlist = []
        for node in self.nodes:
            if node.fixed:
                self.currentlist.append(node.value)
            else:
                self.currentlist.append(None)
        return self.currentlist

    def get_list_as_string(self):
        nodevaluelist = self.get_list()
        return str(nodevaluelist)

    def run_reduce_loop(self):
        global reducenodetime
        global reducercstime
        reducedsomething = False
        if self.reducedtovaluelastloop:
            looptime = time.time()
            self.reducedtovaluelastloop = False
            for i in range(81):
                reducedforelem = False
                reducedtovalelement = False
                if self.nodes[i].value is None:
                    reducedforelem = self.nodes[i].reduceSet()
                    if len(self.nodes[i].allowed_set) ==1:
                        reducedtovalelement = True
                reducedsomething = reducedsomething or reducedforelem
                self.reducedtovaluelastloop = self.reducedtovaluelastloop or reducedtovalelement
            reducenodetime += time.time() - looptime
        else:
            looptime = time.time()
            reducedtoval = False
            reducedsomething = False
            for i in range(9):
                reducedtovalforrow = False
                reducedforrow = False
                if not self.rows[i].isfixed():
                    (reducedtovalforrow,reducedforrow) = self.rows[i].reduce_subsets()
                reducedtoval = reducedtoval or reducedtovalforrow
            if not reducedtoval:
                for i in range(9):
                    reducedtovalforcol = False
                    reducedforcol = False
                    if not self.cols[i].isfixed():
                        (reducedtovalforcol,reducedforcol) = self.cols[i].reduce_subsets()
                    reducedtoval = reducedtoval or reducedtovalforcol
            if not reducedtoval:
                for i in range(9):
                    reducedtovalforsq = False
                    reducedforsq = False
                    if not self.squares[i].isfixed():
                        (reducedtovalforsq,reducedforsq) = self.squares[i].reduce_subsets()
                    reducedsomething = reducedsomething or reducedforsq
            reducercstime += time.time() - looptime

        return reducedsomething

    def __deepcopy__(self):
        result = Sudoku(self.get_list())
        for i in range(81):
            result.nodes[i].allowed_set = self.nodes[i].allowed_set.copy()
            result.nodes[i].value = self.nodes[i].value
            result.nodes[i].fixed = self.nodes[i].fixed
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
        global rcsbuildtime
        global nodebuildtime
        looptime = time.time()
        for i in range(9):
            newrow = Row()
            self.rows.append(newrow)
            newcol = Col()
            self.cols.append(newcol)
            newsq = Square()
            self.squares.append(newsq)
        rcsbuildtime += time.time() - looptime
        looptime = time.time()
        for i in range(81):
            looptime = time.time()
            newnode = Node(input_matrix[i])
            nodebuildtime += time.time() - looptime
            #if input_matrix[i]: newnode = Node(input_matrix[i]) #isinstance(input_matrix[i], int):                newnode = Node(input_matrix[i])
            self.nodes.append(newnode)
            inlooptime = time.time()
            self.rows[i // 9].add_node(newnode)
            self.cols[i % 9].add_node(newnode)
            self.squares[((i // 27) * 3) + ((i % 9) // 3)].add_node(newnode)
            rcsbuildtime += time.time() - inlooptime
        nodebuildtime += time.time() - looptime
        buildtime += time.time() - buildtimest


class Row(list):

    def __init__(self, memberslist=None):
        if memberslist is not None: self += memberslist
        self.fixed = False

    def add_node(self, node):
        self.append(node)
        node.row = self

    def get_elems(self):
        return list(self)

    def reduce(self):
        for elem in self:
            elem.reduceSet()

    def isfixed(self):
        self.fixed = False
        elemset = set()
        for elem in self:
            if elem.value is not None:
                elemset.add(elem.value)
        if elemset == set(range(1, 10)):
            self.fixed = True
        return self.fixed

    def is_filled(self):
        self.filled = False
        for elem in self:
            if not elem.filled:
                return self.filled
        else:
            self.filled = True
            return self.filled

    def reduce_subsets(self):
        subsetlentocheck = 1
        notfixedelems = set([])
        reducedtoval = False
        reducedelem = False
        for i in range(len(self)):
            if len(self[i].allowed_set) > 1:
                notfixedelems.add(i)
        while subsetlentocheck < len(notfixedelems) and len(notfixedelems) > 2 and not reducedtoval:
            for subset in combinations(notfixedelems,subsetlentocheck):
                elemset = set([])
                for node in subset:
                    elemset = elemset.union(self[node].allowed_set)
                if len(elemset) == subsetlentocheck:
                    for notsubsetelem  in notfixedelems.difference(subset):
                        startelemsetlen = len(self[notsubsetelem].allowed_set)
                        if len(self[notsubsetelem].allowed_set) != 1:
                            self[notsubsetelem].allowed_set = self[notsubsetelem].allowed_set.difference(elemset)
                        if len(self[notsubsetelem].allowed_set) <startelemsetlen:
                            reducedelem = True
                        if len(self[notsubsetelem].allowed_set) == 1:
                            reducedtoval = True
                            self[notsubsetelem].updateneighbours()

                    if reducedtoval: break
            if reducedtoval: break
            notfixedelems = set([])
            for i in range(len(self)):
                if len(self[i].allowed_set) > 1:                notfixedelems.add(i)
            subsetlentocheck +=1
        reducedelem = reducedtoval or reducedelem
        return (reducedtoval,reducedelem)





class Col(list):
    def __init__(self, memberslist=None):
        if memberslist is not None: self += memberslist
        self.fixed = False

    def add_node(self, node):
        self.append(node)
        node.col = self

    def get_elems(self):
        return list(self)

    def reduce(self):
        for elem in self:
            elem.reduceSet()

    def isfixed(self):
        self.fixed = False
        elemset = set()
        for elem in self:
            if elem.value is not None:
                elemset.add(elem.value)
        if elemset == set(range(1, 10)):
            self.fixed = True
        return self.fixed

    def is_filled(self):
        self.filled = False
        for elem in self:
            if not elem.filled:
                return self.filled
        else:
            self.filled = True
            return self.filled

    def reduce_subsets(self):
        subsetlentocheck = 1
        notfixedelems = set([])
        reducedtoval = False
        reducedelem = False
        for i in range(len(self)):
            if len(self[i].allowed_set) > 1:
                notfixedelems.add(i)
        while subsetlentocheck < len(notfixedelems) and len(notfixedelems) > 2 and not reducedtoval:
            for subset in combinations(notfixedelems,subsetlentocheck):
                elemset = set([])
                for node in subset:
                    elemset = elemset.union(self[node].allowed_set)
                if len(elemset) == subsetlentocheck:
                    for notsubsetelem  in notfixedelems.difference(subset):
                        startelemsetlen = len(self[notsubsetelem].allowed_set)
                        if len(self[notsubsetelem].allowed_set) != 1:
                            self[notsubsetelem].allowed_set = self[notsubsetelem].allowed_set.difference(elemset)
                        if len(self[notsubsetelem].allowed_set) <startelemsetlen:
                            reducedelem = True
                        if len(self[notsubsetelem].allowed_set) == 1:
                            reducedtoval = True
                            self[notsubsetelem].updateneighbours()

                    if reducedtoval: break
            if reducedtoval: break
            notfixedelems = set([])
            for i in range(len(self)):
                if len(self[i].allowed_set) > 1:                notfixedelems.add(i)
            subsetlentocheck +=1
        reducedelem = reducedtoval or reducedelem
        return (reducedtoval,reducedelem)


class Square(list):
    def __init__(self, memberslist=None):
        if memberslist is not None: self += memberslist
        self.fixed = False


    def add_node(self, node):
        self.append(node)
        node.square = self

    def get_elems(self):
        return list(self)

    def reduce(self):
        for elem in self:
            elem.reduceSet()

    def isfixed(self):
        self.fixed = False
        elemset = set()
        for elem in self:
            if elem.value is not None:
                elemset.add(elem.value)
        if elemset == set(range(1, 10)):
            self.fixed = True
        return self.fixed

    def is_filled(self):
        self.filled = False
        for elem in self:
            if not elem.filled:
                return self.filled
        else:
            self.filled = True
            return self.filled

    def reduce_subsets(self):
        subsetlentocheck = 1
        notfixedelems = set([])
        reducedtoval = False
        reducedelem = False
        for i in range(len(self)):
            if len(self[i].allowed_set) > 1:
                notfixedelems.add(i)
        while subsetlentocheck < len(notfixedelems) and len(notfixedelems) > 2 and not reducedtoval:
            for subset in combinations(notfixedelems,subsetlentocheck):
                elemset = set([])
                for node in subset:
                    elemset = elemset.union(self[node].allowed_set)
                if len(elemset) == subsetlentocheck:
                    for notsubsetelem  in notfixedelems.difference(subset):
                        startelemsetlen = len(self[notsubsetelem].allowed_set)
                        if len(self[notsubsetelem].allowed_set) != 1:
                            self[notsubsetelem].allowed_set = self[notsubsetelem].allowed_set.difference(elemset)
                        if len(self[notsubsetelem].allowed_set) <startelemsetlen:
                            reducedelem = True
                        if len(self[notsubsetelem].allowed_set) == 1:
                            reducedtoval = True
                            self[notsubsetelem].updateneighbours()

                    if reducedtoval: break
            if reducedtoval: break
            notfixedelems = set([])
            for i in range(len(self)):
                if len(self[i].allowed_set) > 1:                notfixedelems.add(i)
            subsetlentocheck +=1
        reducedelem = reducedtoval or reducedelem
        return (reducedtoval,reducedelem)

class Node(object):
    def __init__(self, value=None):
        self.value = value
        self.checkinits()
        #self.row = None
        #self.col = None
        #self.square = None

    def checkinits(self):
        if self.value:
            self.allowed_set = set([self.value])
            self.fixed = True
        else:
            self.allowed_set = set(range(1, 10))
            self.fixed = False

    def updateneighbours(self):
        for elem in self.row:
            if elem is not self:            elem.allowed_set.discard(self.value)
        for elem in self.col:
            if elem is not self:            elem.allowed_set.discard(self.value)
        for elem in self.square:
            if elem is not self:            elem.allowed_set.discard(self.value)

    def checkFixed(self):
        if len(self.allowed_set) == 1 and not self.fixed:
            self.fixed = True
            self.value = tuple(self.allowed_set)[0]
            return self.fixed
        else:
            return self.fixed

    def reducebyrow(self):
        if not self.fixed:
            for elem in self.row:
                if elem.fixed and elem is not self:
                    self.allowed_set.discard(elem.value)
            self.checkFixed()
        if not self.fixed:
            othersunion = set([])
            for elem in self.row:
                if elem is not self:
                    othersunion = othersunion.union(elem.allowed_set)
            remainset = set(range(1,10)).difference(othersunion)
            if len(remainset) == 1:
                self.allowed_set = remainset
                self.fixed = True
                self.value = tuple(remainset)[0]
            self.checkFixed()

    def reducebycol(self):
        if self.col is not None and not self.fixed:
            for elem in self.col:
                if elem.fixed and elem is not self:
                    self.allowed_set.discard(elem.value)
            self.checkFixed()
        if self.col is not None and not self.fixed:
            othersunion = set([])
            for elem in self.col:
                if elem is not self:
                    othersunion = othersunion.union(elem.allowed_set)
            remainset = set(range(1,10)).difference(othersunion)
            if len(remainset) == 1:
                self.allowed_set = remainset
                self.fixed = True
                self.value = tuple(remainset)[0]
            self.checkFixed()

    def reducebysquare(self):
        if self.square is not None and not self.fixed:
            for elem in self.square:
                if elem.fixed and elem is not self:
                    self.allowed_set.discard(elem.value)
            self.checkFixed()
        if self.square is not None and not self.fixed:
            othersunion = set([])
            for elem in self.square:
                if elem is not self:
                    othersunion = othersunion.union(elem.allowed_set)
            remainset = set(range(1,10)).difference(othersunion)
            if len(remainset) == 1:
                self.allowed_set = remainset
                self.fixed = True
                self.value = tuple(remainset)[0]
            self.checkFixed()

    def reduceSet(self):
        initialfix = len(self.allowed_set)
        self.reducebyrow()
        self.reducebycol()
        self.reducebysquare()
        if len(self.allowed_set) ==1:
            self.fixed = True
            self.value = tuple(self.allowed_set)[0]
        return len(self.allowed_set) < (initialfix)

    def set_square(self, square):
        self.square = square

    def get_square(self):
        return self.square

    def set_row(self, row):
        self.row = row

    def get_row(self):
        return self.row

    def set_col(self, col):
        self.col = col

    def get_col(self):
        return self.col


def reduceall(sudokuObject):
    reducedsomething = True
    while reducedsomething:
        reducedsomething = sudokuObject.run_reduce_loop()
    if sudokuObject.checksolved():
        return sudokuObject
    elif sudokuObject.checkfilled():
        return None
    else:
        minnode = sudokuObject.getmin_unfillednode()
        if len(minnode.allowed_set) == 0: return None
        for permuted in (minnode.allowed_set):
            global numsudokuobjects
            numsudokuobjects +=1
            minnode.allowed_set = set([permuted])
            minnode.value = permuted
            minnode.fixed = True
            newsudokuObject = sudokuObject.__deepcopy__()
            solvediteration = reduceall(newsudokuObject)
            if solvediteration is not None: return solvediteration
        return None


def run_sudokusolver(input_string):
    input_list = []
    sudoobj = None
    for char in input_string:
        input_list.append(int(char)) if char != '.' else input_list.append(None)
    sudoobj = Sudoku(input_list)
    sudoobj = reduceall(sudoobj)
    return sudoobj.get_list_as_string()


if __name__ == "__main__":
    #global numsudokuobjects
    #global buildtime

    starttime = time.time()
    numsudokuobjects = 0
    input_string = '.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ",numsudokuobjects)

    numsudokuobjects = 0
    input_string = '...16...83154896..678...49.45..1287998357..167..69853456....78383..26145.....596.'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ",numsudokuobjects)

    numsudokuobjects = 0
    input_string = '...16...831..896..67....49.45..12..9983.7..167..698..456....78383..26145.....596.'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ",numsudokuobjects)

    numsudokuobjects = 0
    input_string = '48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ",numsudokuobjects)

    numsudokuobjects = 0
    input_string = '....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...'
    print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ",numsudokuobjects)

    print("time taken = ",time.time()-starttime)

    numsudokuobjects = 0
    #starttime = time.time()
    toughsudokufile = filename = 'data/toughsudokupuzzles.txt'
    sudokupuzzles =[]
    with open(toughsudokufile) as inputfile:
        for line in inputfile:
            sudokupuzzles.append(line.strip())
    puzzleno = 1
    for puzzle in sudokupuzzles:
        run_sudokusolver(puzzle)
        #print(run_sudokusolver(puzzle))
        puzzleno +=1
        #if puzzleno ==5: break
    print("time taken = ",time.time()-starttime)
    print("build time taken = ",buildtime)
    print("rcs buildtime = ",rcsbuildtime)
    print("node buildtime = ",nodebuildtime)
    print("reduce rcs time taken = ",reducercstime)
    print("reduce node time taken = ",reducenodetime)
    print("number of sudoku objects created = ",numsudokuobjects)


