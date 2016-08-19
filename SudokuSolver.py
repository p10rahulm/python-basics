from math import sqrt

class Sudoku(object):
    def __init__(self, input_list):
        self.input_list = input_list
        sidelength = int(sqrt(len(input_list)))
        #self.input_matrix = [[input_list[k * sidelength + j] for j in range(sidelength)] for k in range(sidelength)]
        self.build_matrix(self.input_list)
        self.checksolved()

    def getmin_unfillednode(self):
        minnode = None
        lenmin = 9
        for node in self.nodes:
            if len(node.allowed_set)!=1 and len(node.allowed_set)<lenmin:
                lenmin=len(node.allowed_set)
                minnode = node
        return minnode


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
        reducedsomething = False
        for i in range(81):
            reducedforelem = False
            if self.nodes[i].value is None:
                # if(len(self.nodes[i].allowed_set) > 0):                    print("i=",i,"self.nodes[i].allowed_set=",self.nodes[i].allowed_set);                    print("self.nodes[i]",self.nodes[i])
                reducedforelem = self.nodes[i].reduceSet()
            reducedsomething = reducedsomething or reducedforelem
        return reducedsomething

    def build_matrix(self, input_matrix):
        self.rows = []
        self.cols = []
        self.squares = []
        self.nodes = []
        for i in range(9):
            newrow = Row()
            self.rows.append(newrow)
            newcol = Col()
            self.cols.append(newcol)
            newsq = Square()
            self.squares.append(newsq)
        for i in range(81):
            newnode = Node()
            if isinstance(input_matrix[i], int):                newnode = Node(input_matrix[i])
            self.nodes.append(newnode)
            self.rows[i // 9].add_node(newnode)
            self.cols[i % 9].add_node(newnode)
            self.squares[((i // 27) * 3) + ((i % 9) // 3)].add_node(newnode)
            # print("newnode.col = ",newnode.col,"newnode.value = ",newnode.value,"newnode.allowed_set = ",newnode.allowed_set)
            # for i in range(81):            print("self.nodes[i].allowed_set",self.nodes[i].allowed_set)


class Row(list):
    def __init__(self, memberslist=[]):
        self.members = memberslist
        self.size = len(memberslist)
        self.is_filled()

    def add_node(self, node):
        self.append(node)
        self.members.append(node)
        node.row = self

    def get_elems(self):
        return list(self)

    def reduce(self):
        for elem in self.members:
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
        self.fixed = False
        for elem in self.members:
            if not elem.fixed:
                return self.fixed
        else:
            self.fixed = True
            return self.fixed


class Col(list):
    def __init__(self, memberslist=[]):
        self.members = memberslist
        self.size = len(memberslist)
        self.is_filled()

    def add_node(self, node):
        self.append(node)
        self.members.append(node)
        node.col = self

    def get_elems(self):
        return list(self)

    def reduce(self):
        for elem in self.members:
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
        self.fixed = False
        for elem in self:
            if not elem.fixed:
                return self.fixed
        else:
            self.fixed = True
            return self.fixed


class Square(list):
    def __init__(self, memberslist=[]):
        self.members = memberslist
        self.size = len(memberslist)
        self.is_filled()

    def add_node(self, node):
        self.append(node)
        self.members.append(node)
        node.square = self

    def get_elems(self):
        return list(self)

    def reduce(self):
        for elem in self.members:
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
        self.fixed = False
        for elem in self.members:
            if not elem.fixed:
                return self.fixed
        else:
            self.fixed = True
            return self.fixed


class Node(object):
    def __init__(self, value=None):
        self.value = value
        self.checkinits()
        self.fixed = True if len(self.allowed_set) == 1 else False
        self.row = None
        self.col = None
        self.square = None

    def checkinits(self):
        if self.value is not None:
            self.allowed_set = set([self.value])
        else:
            self.allowed_set = set(range(1, 10))

    def checkFixed(self):
        if len(self.allowed_set) == 1:
            self.fixed = True
            self.value = tuple(self.allowed_set)[0]
            return self.fixed
        else:
            return self.fixed

    def reducebyrow(self):
        # if(len(self.allowed_set) > 0):print("inredbyrow lfallowed_set=",self.allowed_set);
        initialfix = self.fixed
        if self.row is not None and self.fixed == False:
            for elem in self.row:
                if elem.fixed and elem is not self:
                    self.allowed_set.discard(elem.value)
            self.checkFixed()
        return self.fixed and not initialfix

    def reducebycol(self):
        initialfix = self.fixed
        if self.col is not None and self.fixed == False:
            for elem in self.col:
                if elem.fixed and elem is not self:
                    self.allowed_set.discard(elem.value)
            self.checkFixed()
        return self.fixed and not initialfix

    def reducebysquare(self):
        initialfix = self.fixed
        if self.square is not None and self.fixed == False:
            for elem in self.square:
                if elem.fixed and elem is not self:
                    self.allowed_set.discard(elem.value)
            self.checkFixed()
        return self.fixed and not initialfix

    def reduceSet(self):
        initialfix = len(self.allowed_set)
        # if(len(self.allowed_set) > 0):print("selfallowed_set=",self.allowed_set);
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
    if sudokuObject.checksolved(): return sudokuObject
    reducedsomething = True
    while reducedsomething:
        reducedsomething = sudokuObject.run_reduce_loop()
    if sudokuObject.checksolved():
        #print("in checksolved")
        return sudokuObject
    elif sudokuObject.checkfilled():
        #print("in checkfilled")
        return None
    else:
        minnode = sudokuObject.getmin_unfillednode()
        if len(minnode.allowed_set) == 0: return None
        #print("minnode=",minnode,"allowed_set = ",(minnode.allowed_set))#,"allowedset = ",sudokuObject.nodes[minnode].allowed_set)
        for permuted in (minnode.allowed_set):
            #print("minnode.allowed_set",minnode.allowed_set,"permuted",permuted)
            minnode.allowed_set = set([permuted])
            minnode.value = permuted
            minnode.fixed = True
            newsudokuObject = Sudoku(sudokuObject.get_list())
            # print("inside","sudokuObject.nodes[minnode].value = ",sudokuObject.nodes[minnode].value,"sudokuObject.nodes[minnode].allowed_set = ",sudokuObject.nodes[minnode].allowed_set)
            solvediteration = reduceall(newsudokuObject)
            #print("solvediteration=", solvediteration)
            if solvediteration is not None: return solvediteration

        return None


def run_sudokusolver(input_string):
    input_list = []
    sudoobj = None
    for char in input_string:
        input_list.append(int(char)) if char != '.' else input_list.append(None)
    sudoobj = Sudoku(input_list)
    # print(sudoobj.get_list_as_string())
    sudoobj = reduceall(sudoobj)
    # if sudoobj.checksolved():
    return sudoobj.get_list_as_string()


if __name__ == "__main__":
    import time
    starttime = time.time()
    input_string = '.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8'
    print(run_sudokusolver(input_string))

    input_string = '...16...83154896..678...49.45..1287998357..167..69853456....78383..26145.....596.'
    print(run_sudokusolver(input_string))

    input_string = '...16...831..896..67....49.45..12..998357..167..698..456....78383..26145.....596.'
    print(run_sudokusolver(input_string))

    input_string = '48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....'
    print(run_sudokusolver(input_string))

    input_string = '....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...'
    print(run_sudokusolver(input_string))

    print("time taken = ",time.time()-starttime)

    '''
    starttime = time.time()
    toughsudokufile = filename = 'data/toughsudokupuzzles.txt'
    sudokupuzzles =[]
    with open(toughsudokufile) as inputfile:
        for line in inputfile:
            sudokupuzzles.append(line.strip())
    for puzzle in sudokupuzzles:
        print(run_sudokusolver(puzzle))
    print("time taken = ",time.time()-starttime)
    '''
