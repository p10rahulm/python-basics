def prefixtoinfix(mystr):
    queuedopers = []
    queuedexprs = []
    allowed_operators = ['+','-','*','/','**','^','%']
    i =0
    mystr = mystr[::-1]
    while i != len(mystr):
        if mystr[i] in allowed_operators: queuedopers.append(mystr[i])
        else: queuedexprs.append(mystr[i])
        while len(queuedexprs) >=2 and len(queuedopers)>0:
                a = queuedexprs.pop(-1)
                b = queuedexprs.pop(-1)
                infix_opr = queuedopers.pop(-1)
                queuedexprs.append("(" + a + infix_opr + b + ")")
        i+=1
    return queuedexprs[0]

if __name__ == "__main__":
    print("test 1")
    print(prefixtoinfix("/+2b-3a"))
