import sys
import copy

x = 27

def unify(var, queryargs, theta):
    #print "entered unify", len(var), var, queryargs
    for i in range(len(var)):
        isFirstVar = var[i].islower()
        isSecondVar = queryargs[i].islower()
        if not isFirstVar and not isSecondVar:
            #print "branch 1"
            if var[i] != queryargs[i]:
                return None
        elif isFirstVar and isSecondVar:
            if queryargs[i] == var[i]:
                return theta
            #print "branch 2"
            if not queryargs[i] in theta:
                theta[queryargs[i]] = var[i]
            else:
                tmp = queryargs[i]
                while tmp in theta:
                    tmp = theta[tmp]
                if (tmp.islower()):
                    theta[var[i]] = queryargs[i]
                else:
                    theta[var[i]] = tmp
        elif isFirstVar and not isSecondVar:
            #print "branch 3"
            theta[var[i]] = queryargs[i]
        else:
            #print "branch 4"
            #print theta, queryargs[i], var[i]
            if not queryargs[i] in theta:
                #print "here"
                theta[queryargs[i]] = var[i]
            else:
                tmp = queryargs[i]
                while tmp in theta:
                    tmp = theta[tmp]
                if (tmp.islower()):
                    theta[queryargs[i]] = var[i]
                else:
                    if tmp != var[i]:
                        return None

            #print "cur theta:  ", theta
    #print "after unify:", theta
    return theta    
    '''
    print "in unify"
    print "queryargs:", queryargs
    print "goalargs:", goalargs
    if theta == None:
        return None
    elif queryargs == goalargs:
        return theta
    elif len(queryargs) == 1 and queryargs[0].islower():    #queryargs is a variable
        return unify_var(queryargs[0], goalargs, theta)
    elif len(goalargs) == 1 and goalargs[0].islower():    #goalarg is a variable
        return unify_var(goalargs[0], queryargs, theta)
    elif len(queryargs) > 1 and len(goalargs) > 1:    #queryargs and goalargs are lists
        return unify(queryargs[1:], goalargs[1:],unify(queryargs[0], goalargs[0], theta))
    else:
        return None    #return failure
    '''


def unify_var(var, queryargs, theta):
    #print "hahaha" + var[0]
    #print "hehehe" , queryargs
    for i in range(len(var)):
        isFirstVar = var[i].islower()
        isSecondVar = queryargs[i].islower()
        if not isFirstVar and not isSecondVar and var[i] != queryargs[i]:
            return None
        elif isFirstVar and isSecondVar:
            theta[var[i]] = queryargs[i]
        elif isFirstVar and not isSecondVar:
            theta[var[i]] = queryargs[i]
        else:
            theta[queryargs[i]] = var[i]
            #print "cur theta:  ", theta
    #print "after unify var:", theta
    return theta    

def subst(theta, first):    #dict, predicate. return the result of the corresponding implementation of unify
    #print "in subst"
    #print "before subst: theta is", theta
    first_args = first[first.find("(") + 1: first.find(")")].split(', ')
    first_name = first.split('(')[0]
    for i in range(len(first_args)):
        if first_args[i] in theta:
            first_args[i] = theta[first_args[i]]    #substitute
    first = first_name + '('
    for i in range(len(first_args)):
        first = first + first_args[i]
        if i + 1 < len(first_args):
            first = first + ', '
    first = first + ')'
    #f1.write("in subst: " + "True: " + first + '\r\n')
    #print("in subst: " + "True: " + first + '\r\n')
    return first



def get_Unused_Var():
    global x
    res = ""
    n = x
    x = x + 1
    while (n > 0):
        n = n - 1
        res = chr(ord('a') + (n % 26)) + res
        n /= 26
    #print "get_Unused_Var:", res, type(res)
    return res
#print "testtesttest:  ", get_Unused_Var(27)

def stdVar(lhs, rhs, usedVars):    #goalargs and rhsargs have the same length and corresponding positions
    lhs_res = []
    rhs_res = []
    rhsargs = rhs[rhs.find("(") + 1: rhs.find(")")].split(', ')
    rhsname = rhs.split('(')[0]
    addedVars = {}
    tmpset = set()
    for i in range(len(lhs)):
        lhsargs = lhs[i][lhs[i].find("(") + 1: lhs[i].find(")")].split(', ')
        for j in range(len(lhsargs)):
            if lhsargs[j].islower():
                if lhsargs[j] in usedVars:
                    if lhsargs[j] not in addedVars:
                        addedVars[lhsargs[j]] = get_Unused_Var()
                else:
                    tmpset.add(lhsargs[j])
    usedVars.update(tmpset)
    #print "tmpset:", tmpset
    #print "usedVars:", usedVars
    #print "addedVars:", addedVars

    for i in range(len(lhs)):
        lhsname = lhs[i].split('(')[0]
        temp = str(lhsname) + '('

        lhsargs = lhs[i][lhs[i].find("(") + 1: lhs[i].find(")")].split(', ')    #extract the args of each conjunciton
        for k in range(len(lhsargs)):
            temp += addedVars.get(lhsargs[k], lhsargs[k]) + ", "

        temp = temp[:-2] + ')'
        lhs_res.append(temp)
    #print "lhs_res:", lhs_res

    temp = str(rhsname) + '(' 
    for i in range(len(rhsargs)):
        temp += addedVars.get(rhsargs[i], rhsargs[i]) + ", "
    temp = temp[:-2] + ')'
    rhs_res = temp
    #print "rhs: ", temp
    #print "stdVar ended for", lhs_res, rhs_res
    return lhs_res, rhs_res

    ''' 
    for i in range(len(lhs)):
        lhsargs = lhs[i][lhs[i].find("(") + 1: lhs[i].find(")")].split(', ')    #extract the args of each conjunciton
        for j in range(len(lhsargs)):
            for k in range(len(goalargs)):
                if lhsargs[j].islower() and (lhsargs[j] == goalargs[k]):
                    lhsargs[j] = get_Unused_Var(n)
                    n = n + 1
    for i in range(len(lhs)):
        lhsname = lhs[i].split('(')[0]
        temp = str(lhsname) + '('
        lhsargs = lhs[i][lhs[i].find("(") + 1: lhs[i].find(")")].split(', ')    #extract the args of each conjunciton
        for k in range(len(lhsargs)):
            for j in range(len(rhsargs)):
                if lhsargs[k].islower() and (lhsargs[k] == rhsargs[j]):
                    lhsargs[k] = goalargs[j]
            temp = temp + lhsargs[k]
            if k + 1 < len(lhsargs):
                temp = temp + ', '
        temp = temp + ')'
        print "temp in loop: ", temp
        lhs_res.append(temp)

    print "lhs_res: ", lhs_res

    temp = str(rhsname) + '(' 
    for i in range(len(rhsargs)):
        if rhsargs[i].islower() and goalargs[i].islower():
            rhsargs[i] = goalargs[i]
        temp = temp + rhsargs[i]
        if i + 1 < len(rhsargs):
            temp = temp + ', '
    temp = temp + ')'
    rhs_res = temp
    print "rhs: ", temp
    return lhs_res, rhs_res
    '''
def writeAsk(goal):
    goalargs = goal[goal.find("(") + 1: goal.find(")")].split(', ')
    goalname = goal.split('(')[0]
    tmpargs = goalname + '('
    for i in range(len(goalargs)):
        if goalargs[i].islower():
            goalargs[i] = '_'
        tmpargs = tmpargs + goalargs[i]
        if i + 1 < len(goalargs):
            tmpargs = tmpargs + ', '
    tmpargs = tmpargs + ')'
    f1.write("Ask: " + tmpargs + '\n')

def writeTrue(first):
    goalargs = first[first.find("(") + 1: first.find(")")].split(', ')
    goalname = first.split('(')[0]
    tmpargs = goalname + '('
    for i in range(len(goalargs)):
        if goalargs[i].islower():
            goalargs[i] = '_'
        tmpargs = tmpargs + goalargs[i]
        if i + 1 < len(goalargs):
            tmpargs = tmpargs + ', '
    tmpargs = tmpargs + ')'
    f1.write("True: " + tmpargs + '\n')

def bc_ask(KB, query):
    
    return bc_or(KB, query, {}, set())

def bc_ask_and(KB, queries):
    return bc_and(KB, queries, {}, set())

def bc_or(KB, goal, theta, usedVars):    #goal is a str #yields a substitution
    #print "in bc_or:   " + goal
    kbs = []
    facts = []
    imps = []
    goalname = goal.split('(')[0]    #extract name of the goal
    goalargs = goal[goal.find("(") + 1: goal.find(")")].split(', ')
    writeAsk(goal)
    #f1.write("Ask: " + goal + '\n')
    #print "bc_or goalargs:   ", goalargs
    if goalname in KB[0]:
        facts = KB[0][goalname]    #a list of instances
    if goalname in KB[1]:
        imps = KB[1][goalname]    #a list of instances 
    for i in range(len(facts)):
        kbs.append(facts[i])
    for i in range(len(imps)):
        kbs.append(imps[i])
    for i in range(len(kbs)):
        onerhs = kbs[i].conclusion    #onerhs is a str e.g.Aunt(a,b)
        onelhs = kbs[i].conditions    #onelhs is a list of predicates
        #print "cmz: onerhs", onerhs, type(onerhs)
        #print "cmz: onelhs", onelhs, type(onelhs)
        #print "bc_or origins:   ", onelhs, onerhs
        usedVarsCopy = copy.deepcopy(usedVars)
        onelhs, onerhs = stdVar(onelhs, onerhs, usedVars)
        #print "bc_or stdizeVar:   ", onelhs, onerhs, "type(onerhs):", type(onerhs)
        onerhs_args = onerhs[onerhs.find("(") + 1: onerhs.find(")")].split(', ')
        #print "onerhs_args:", onerhs_args
        #print "goalargs:", goalargs
        theta_copy = copy.deepcopy(theta)
        for thetaP in bc_and(KB, onelhs, unify(onerhs_args, goalargs, theta_copy), usedVars):
            yield thetaP


def bc_and(KB, goals, theta, usedVars):    #yields a substitution
    if theta == None:
        #print 'failed'
        return
    elif len(goals) == 0:
        yield theta
    else:
        first = goals[0]    #a predicate
        rest = goals[1:]    #list of predicates
        #print "in bc_and:", first

        #print "bc_and first:  ", first
        #print "bc_and rest: ", rest
        #theta = copy.deepcopy(theta)
        #goal_subst = subst(theta, first)
        #print "aaaaaaaaaaaaaaaaaaaa   " + goal_subst
        for thetaP in bc_or(KB, subst(theta, first), theta, usedVars):
            #thetaP_copy = copy.deepcopy(thetaP)
            writeTrue(first)
            #f1.write("True: " + first + "\n")
            for thetaPP in bc_and(KB, rest, thetaP, usedVars):
                yield thetaPP


'''read command'''
assert sys.argv[1] == "-i"
filename = sys.argv[2]
f = open(filename)

finaltar = f.readline().strip().split(' && ')
#print finaltar
finale = ""
if len(finaltar) == 1:
    finale = finaltar[0]
number = int(f.readline().strip())

class Implication():
    def __init__(self, conditions, conclusion):
        self.conditions = conditions    #e.g. [Woman(c), Siblings(c, e), Parent(c, d)]
        self.conclusion = conclusion    #e.g. Aunt(c,d)

class Predicate():
    def __init__(self, name, predicate, isFact):
        self.name = name                #e.g. Aunt       Parent
        self.predicate = predicate      #e.g. Aunt(c,d)  Parent(Kevin, Jane)
        self.isAtomic = isFact


Facts = {}    #for atomic sentence
Rules = {}    #for implications
for i in range(number):
    sentence = f.readline().strip()
    if "=>" in sentence:    #with implication
        terms = sentence.split(' => ')
        lhs = list(terms[0].split(' && '))
        for i in range(len(lhs)):    #handle all the premises
            oneconj = lhs[i]
            conjname = oneconj.split('(')[0]
            onepredicate = Predicate(conjname, oneconj, False)
        rhs = terms[1]
        rhsname = rhs.split('(')[0]
        onepredicate = Predicate(rhsname, rhs, False)
        onerule = Implication(lhs, rhs)
        Rules.update({rhs: lhs})    #a rule add to KB
        if rhsname in Rules:
            Rules[rhsname].append(onerule)
            #print "key:" + rhsname
            #print Rules[rhsname][0].conditions
        else:
            Rules.update({rhsname: [onerule]})
            #print "key:" + rhsname
            #print Rules[rhsname][0].conditions

    else:    #atomic sentence
        name = sentence.split('(')[0]
        onefact = Predicate(name, sentence, True)
        onerule = Implication([], sentence)
        if name in Facts:
            Facts[name].append(onerule)
            #print "key:" + name
            #print Facts[name][0].conclusion
        else:
            Facts.update({name: [onerule]})
            #print "key:" + name
            #print Facts[name][0].conclusion
        
f.close()


KB = [Facts, Rules]
f1 = open('output.txt', 'w')
isValid = True
entered = False
if len(finaltar) == 1:
    for res in bc_ask(KB, finale):
        entered = True
        #print "final:", res
        if res is None:
            f1.write("False: " + finale + "\n")
            f1.write("False")
            #print "False"
            isValid = False
            break

    if entered:
        if isValid:
            f1.write("True: " + finale + "\n")
            f1.write("True")
            #print "True"
    else:
        f1.write("False: " + finale + "\n")
        f1.write("False")
        #print "False"
    f1.close()
else:
    for res in bc_ask_and(KB, finaltar):
        entered = True
        #print "final:", res
        if res is None:
            #f1.write("False: " + finale + "\n")
            f1.write("False")
            #print "False"
            isValid = False
            break

    if entered:
        if isValid:
            #f1.write("True: " + finale + "\n")
            f1.write("True")
            #print "True"
    else:
        #f1.write("False: " + finale + "\n")
        f1.write("False")
        #print "False"
    f1.close()
