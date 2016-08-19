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
        self.build_matrix(self.input_list)
        self.solved = False
        self.reducedtovaluelastloop = True

    def getmin_unfillednode(self):
        minnode = None
        lenmin = 9
        #print("mystr",self.get_list_as_string())
        for node in self.nodes:
            if len(node.allowedset)> 1 and len(node.allowedset)<lenmin:
                lenmin=len(node.allowedset)
                minnode = node
        return minnode

    def shownodeslist(self):
        mylist = []
        for i in range(len(self.nodes)):
            mylist.append(self.nodes[i].allowedset)
        print(mylist)

    def checksolved(self):
        #print("in checksolved")
        solved = True
        for row in self.rows:
            if not row.isfixed():
                #print("row is not fixed",)
                #for elem in row: print(elem.allowedset,)

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
            #print("elem = ",elem,"len(elem)=",len(elem.allowedset),"elem")
            if len(elem.allowedset) != 1:
                #print("elem.allowedset",elem.allowedset)
                solved = False
                break
        self.solved = solved
        #print(self.solved,self.nodes[2].allowedset)
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
                if len(self.nodes[i].allowedset) > 1:
                    reducedforelem = self.nodes[i].reducenode()
                    if len(self.nodes[i].allowedset) ==1:
                        reducedtovalelement = True
                        self.nodes[i].updateneighbours()
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
            result.nodes[i].allowedset = result.nodes[i].allowedset.copy()
            #while(len(result.nodes[i].allowedset)): result.nodes[i].allowedset.pop()
            #for j in self.nodes[i]:
            #    result.nodes[i].add(j)
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
            newnode = Node(self.rows[i // 9],self.cols[i % 9],self.squares[((i // 27) * 3) + ((i % 9) // 3)])
            if input_matrix[i] is not None:
                newnode.allowedset.add(input_matrix[i])
            else:
                for j in range(1,10): newnode.allowedset.add(j)
            nodebuildtime += time.time() - looptime
            self.nodes.append(newnode)
            inlooptime = time.time()
            self.rows[i // 9].append(newnode)
            self.cols[i % 9].append(newnode)
            self.squares[((i // 27) * 3) + ((i % 9) // 3)].append(newnode)
            rcsbuildtime += time.time() - inlooptime
        nodebuildtime += time.time() - looptime
        buildtime += time.time() - buildtimest


class Row(list):
    def __init__(self):
        self.fixed = False

    def isfixed(self):
        #print("inside isfixed. len seld is",len(self))
        if not self.fixed :
            #print("inside if not self.fixed")
            elemset = set()
            for elem in self:
                #print(elem.allowedset)
                if len(elem.allowedset) == 1:
                    elemset.add(tuple(elem.allowedset)[0])
            #print("elemset = ",elemset)
            if elemset == set(range(1, 10)):
                self.fixed = True
        return self.fixed

    def reduce_subsets(self):
        subsetlentocheck = 1
        notfixedelems = set([])
        reducedtoval = False
        reducedelem = False
        for i in range(len(self)):
            if len(self[i].allowedset) > 1:
                notfixedelems.add(i)
        while subsetlentocheck < len(notfixedelems) and len(notfixedelems) > 2 and not reducedtoval:
            for subset in combinations(notfixedelems,subsetlentocheck):
                elemset = set([])
                for node in subset:
                    elemset = elemset.union(self[node].allowedset)
                if len(elemset) == subsetlentocheck:
                    for notsubsetelem  in notfixedelems.difference(subset):
                        startelemsetlen = len(self[notsubsetelem].allowedset)
                        if len(self[notsubsetelem].allowedset) != 1:
                            self[notsubsetelem].allowedset = self[notsubsetelem].allowedset.difference(elemset)
                        if len(self[notsubsetelem].allowedset) < startelemsetlen:
                            reducedelem = True
                        if len(self[notsubsetelem].allowedset) == 1:
                            reducedtoval = True
                            self[notsubsetelem].updateneighbours()
                if reducedtoval: break
                notfixedelems = set([])
                for i in range(len(self)):
                    if len(self[i].allowedset) > 1:                notfixedelems.add(i)
            if reducedtoval: break
            subsetlentocheck +=1
        reducedelem = reducedtoval or reducedelem
        return (reducedtoval,reducedelem)





class Col(list):
    def __init__(self, memberslist=None):
        if memberslist is not None: self += memberslist
        self.fixed = False

    def isfixed(self):
        if not self.fixed :
            elemset = set()
            for elem in self:
                if len(elem.allowedset) == 1:
                    elemset.add(tuple(elem.allowedset)[0])
            if elemset == set(range(1, 10)):
                self.fixed = True
        return self.fixed

    def reduce_subsets(self):
        subsetlentocheck = 1
        notfixedelems = set([])
        reducedtoval = False
        reducedelem = False
        for i in range(len(self)):
            if len(self[i].allowedset) > 1:
                notfixedelems.add(i)
        while subsetlentocheck < len(notfixedelems) and len(notfixedelems) > 2 and not reducedtoval:
            for subset in combinations(notfixedelems,subsetlentocheck):
                elemset = set([])
                for node in subset:
                    elemset = elemset.union(self[node].allowedset)
                if len(elemset) == subsetlentocheck:
                    for notsubsetelem  in notfixedelems.difference(subset):
                        startelemsetlen = len(self[notsubsetelem].allowedset)
                        if len(self[notsubsetelem].allowedset) != 1:
                            self[notsubsetelem].allowedset = self[notsubsetelem].allowedset.difference(elemset)
                        if len(self[notsubsetelem].allowedset) < startelemsetlen:
                            reducedelem = True
                        if len(self[notsubsetelem].allowedset) == 1:
                            reducedtoval = True
                            self[notsubsetelem].updateneighbours()
                if reducedtoval: break
                notfixedelems = set([])
                for i in range(len(self)):
                    if len(self[i].allowedset) > 1:                notfixedelems.add(i)
            if reducedtoval: break
            subsetlentocheck +=1
        reducedelem = reducedtoval or reducedelem
        return (reducedtoval,reducedelem)




class Square(list):
    def __init__(self, memberslist=None):
        if memberslist is not None: self += memberslist
        self.fixed = False

    def isfixed(self):
        if not self.fixed :
            elemset = set()
            for elem in self:
                if len(elem.allowedset) == 1:
                    elemset.add(tuple(elem.allowedset)[0])
            if elemset == set(range(1, 10)):
                self.fixed = True
        return self.fixed

    def reduce_subsets(self):
        subsetlentocheck = 1
        notfixedelems = set([])
        reducedtoval = False
        reducedelem = False
        for i in range(len(self)):
            if len(self[i].allowedset) > 1:
                notfixedelems.add(i)
        while subsetlentocheck < len(notfixedelems) and len(notfixedelems) > 2 and not reducedtoval:
            for subset in combinations(notfixedelems,subsetlentocheck):
                elemset = set([])
                for node in subset:
                    elemset = elemset.union(self[node].allowedset)
                if len(elemset) == subsetlentocheck:
                    for notsubsetelem  in notfixedelems.difference(subset):
                        startelemsetlen = len(self[notsubsetelem].allowedset)
                        if len(self[notsubsetelem].allowedset) != 1:
                            self[notsubsetelem].allowedset = self[notsubsetelem].allowedset.difference(elemset)
                        if len(self[notsubsetelem].allowedset) < startelemsetlen:
                            reducedelem = True
                        if len(self[notsubsetelem].allowedset) == 1:
                            reducedtoval = True
                            self[notsubsetelem].updateneighbours()
                if reducedtoval: break
                notfixedelems = set([])
                for i in range(len(self)):
                    if len(self[i].allowedset) > 1:                notfixedelems.add(i)
            if reducedtoval: break
            subsetlentocheck +=1
        reducedelem = reducedtoval or reducedelem
        return (reducedtoval,reducedelem)



class Node(object):
    def __init__(self, row,col,square):
        self.row = row
        self.col = col
        self.square = square
        self.allowedset = set([])
        #if value: self.add(value)
        #else:
        #    self = set([])
        #    for i in range(1,10): self.add(i)
        #    print(self)

    def showrowlists(self):
        #print("in show row lists")
        mylist = []
        for elem in self.row:
            mylist.append(elem.allowedset)
        print("self = ",self.allowedset,"row = ",mylist)

    def showcollists(self):
        #print("in show col lists")
        mylist = []
        for elem in self.col:
            mylist.append(elem.allowedset)
        print("self = ",self.allowedset,"col = ",mylist)

    def showsqlists(self):
        #print("in show sq lists")
        mylist = []
        for elem in self.square:
            mylist.append(elem.allowedset)
        print("self = ",self.allowedset,"sq = ",mylist)
    '''
    def updateneighbours(self):
        for elem in self.row:
            if elem is not self:            elem.allowedset.discard(tuple(self.allowedset)[0])
        for elem in self.col:
            if elem is not self:            elem.allowedset.discard(tuple(self.allowedset)[0])
        for elem in self.square:
            if elem is not self:            elem.allowedset.discard(tuple(self.allowedset)[0])
    '''
    def updateneighbours(self):
        #print("in update neigbours", )
        #self.showrowlists()
        #self.showcollists()
        #self.showsqlists()

        for elem in self.row:
            if len(elem.allowedset) > 1 and elem is not self:
                elem.allowedset.discard(tuple(self.allowedset)[0])
                if len(elem.allowedset) == 1:
                    elem.updateneighbours()

        for elem in self.col:
            if len(elem.allowedset) > 1 and elem is not self:
                elem.allowedset.discard(tuple(self.allowedset)[0])
                if len(elem.allowedset) == 1:
                    elem.updateneighbours()

        for elem in self.square:
            if len(elem.allowedset) > 1 and elem is not self:
                elem.allowedset.discard(tuple(self.allowedset)[0])
                if len(elem.allowedset) == 1:
                    elem.updateneighbours()

    def reducenode(self):
        initialfix = len(self.allowedset)
        for elem in self.row:
            if len(elem.allowedset) == 1 and elem is not self and len(self.allowedset)>1:
                self.allowedset.discard(tuple(elem.allowedset)[0])
        if len(self.allowedset)==1: self.updateneighbours()

        for elem in self.col:
            if len(elem.allowedset) == 1 and elem is not self and len(self.allowedset)>1:
                self.allowedset.discard(tuple(elem.allowedset)[0])
        if len(self.allowedset)==1: self.updateneighbours()

        for elem in self.square:
            if len(elem.allowedset) == 1 and elem is not self and len(self.allowedset)>1:
                self.allowedset.discard(tuple(elem.allowedset)[0])

        if len(self.allowedset)==1: self.updateneighbours()
        if len(self.allowedset)>1:
            othersunion = set([])
            for elem in self.row:
                if elem is not self:
                    othersunion = othersunion.union(elem.allowedset)
            remainset = set(range(1,10)).difference(othersunion)
            if len(remainset) == 1: self.allowedset = remainset
            if len(self.allowedset)==1: self.updateneighbours()
        if len(self.allowedset)>1:
            othersunion = set([])
            for elem in self.col:
                if elem is not self:
                    othersunion = othersunion.union(elem.allowedset)
            remainset = set(range(1,10)).difference(othersunion)
            if len(remainset) == 1: self.allowedset = remainset
            if len(self.allowedset)==1: self.updateneighbours()
        if len(self.allowedset)>1:
            othersunion = set([])
            for elem in self.square:
                if elem is not self:
                    othersunion = othersunion.union(elem.allowedset)
            remainset = set(range(1,10)).difference(othersunion)
            if len(remainset) == 1: self.allowedset = remainset
            if len(self.allowedset)==1: self.updateneighbours()
        return len(self.allowedset) < initialfix

def reduceall(sudokuObject):
    reducedsomething = True
    #print("inside reduceall")
    while reducedsomething:
        #print("running reduce loop")
        reducedsomething = sudokuObject.run_reduce_loop()
    #print("out of while")
    if sudokuObject.checksolved():
        return sudokuObject
    elif sudokuObject.checkfilled():
        #print("inside checkfilled",sudokuObject.get_list_as_string())
        return None
    else:
        #print("in blank")
        for i in range(len(sudokuObject.nodes)):
            if len(sudokuObject.nodes[i].allowedset) ==0:
                #print("sudokuObject.nodes[i].allowedset",sudokuObject.nodes[i].allowedset,"i = ",i)
                #print("sudokuObject.get_list_as_string() =",sudokuObject.get_list_as_string())
                return None

        #print("inside random")
        #sudokuObject.shownodeslist()
        minnode = sudokuObject.getmin_unfillednode()
        #minnode.showrowlists()
        #minnode.showcollists()
        #minnode.showsqlists()
        #print(minnode.allowedset)
        if len(minnode.allowedset) == 0:
            return None
        permutor = set()
        for i in minnode.allowedset: permutor.add(i)
        for permuted in permutor:
            #print("in permuted part",minnode,"permuted = ",permuted)
            global numsudokuobjects
            numsudokuobjects +=1
            minnode.allowedset = set([permuted])
            #minnode.value = permuted
            #minnode.fixed = True
            newsudokuObject = sudokuObject.__deepcopy__()
            solvediteration = reduceall(newsudokuObject)
            if solvediteration is not None:
                #print("returning solved iteration")
                return solvediteration
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
    #input_string = '.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8'
    #print(run_sudokusolver(input_string))
    print("number of sudoku objects created = ",numsudokuobjects)

    numsudokuobjects = 0
    input_string = '29416735831548962767825349145631287998357421672169853456294178383972614514783596.'
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


