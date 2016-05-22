import sys
import copy
from decimal import Decimal
assert sys.argv[1] == "-i"
filename = sys.argv[2]

def delComma(arg):
    if len(arg) != 1:
        return tuple(arg)
    else:
        l1 = []
        l2 = []
        for i in arg:
            l1.append(i)
            t = tuple(l1)
            l2.append(t)
            l1 = []
        
        temp = ', '.join('({})'.format(t[0]) for t in l2)
        if temp == '(True)':
            res = True
        else:
            res = False
        
        return res
def extend(e, X, xi):
    e2 = e.copy()
    '''
    print "In extend!!!"
    print "Type of X:", type(X)
    '''
    if len(X) == 0:
        return e2

    if isinstance(X, str):
        e2[X] = xi
    else:
        for i in range(len(xi)):
            e2[X[i]] = xi[i] 
    return e2


def event_values(event, variables):     #dict, list
    eventVals = []
    for var in variables:
        eventVals.append(event[var])
    return delComma(eventVals)

def prob(var, value, event):     # string, bool, dict
    # print "TEST PROB"
    # print bayesnet[var].parents
    parent_vals = event_values(event, bayesnet[var].parents)
    # print "parent_vals:", parent_vals
    ptrue = bayesnet[var].cpt[parent_vals]
    return (ptrue if value else 1 - ptrue)


def normalize(Q):   #dict
    total = 0
    for var in Q:
        total += Q[var]
    # print "total sum is:", total
    for var in Q:
        Q[var] = Q[var]/total
    return Q

def createTrueFalse(numVar):
    res = []
    
    count = 2**numVar
    for i in range(count):
        tmp = []
        for j in range(numVar):
            if ((1 << (numVar-j-1)) & i) == 0:
                tmp.append(True)
            else:
                tmp.append(False)
        res.append(tmp)
    return res


def enumeration_ask(X, e, bn):      # a list, a dict, a dict, a dict
    Q = {}
    for xi in createTrueFalse(len(X)):
        keyName = delComma(xi)
        Q[keyName] = enumeration_all(bnvars, extend(e, X, xi), bn)
    if not X:
        return Q
    else:
        Q = normalize(Q)
        return Q


def enumeration_all(variables, e, bn):   # a list, a dict, a dict.  return a real value
    if not variables:
        return 1.0
    Y, rest = variables[0], variables[1:]
    
    if Y in e:
        return prob(Y, e[Y], e) * enumeration_all(rest, e, bn)
    else:
       
        return sum(prob(Y, y, e) * enumeration_all(rest, extend(e, Y, y), bn) for y in [True, False])



def mergeToDict(argKey, argVal):    #arg1 and arg2 should have the same len
    myDict = {}
    if isinstance(argVal, bool):
        myDict[argKey[0]] = argVal
        return myDict
    for i in range(len(argKey)):
        myDict[argKey[i]] = argVal[i]
    return myDict


def mergeDictsInOrder(keyName, tmpDict, myDict):    #dict, dict, dict. return a dict in the order of myDict
    res = {}
    for var in myDict:
        if var in tmpDict:
            res[var] = tmpDict[var]
        else:
            res[var] = keyName[var]
    return res


def utility(utilInfo, utilVars, normalizedQ, p_varnames, keyName):     # dict, list, dict, list, dict
    myDict = {}
    utilVarEvent = []
    res = 0
    for var in utilVars:
        myDict[var] = True
    for eachKey in normalizedQ:     #eachKey is a tuple
        utilVarEvent = []
        prob = normalizedQ[eachKey]
        tmpDict = mergeToDict(p_varnames, eachKey)
        # print "tmpDict is: ", tmpDict
        # print "keyName is: ", keyName
        myDict = mergeDictsInOrder(tmpDict, keyName, myDict)
        #print "myDict is: ", myDict
        for var in utilVars:
            utilVarEvent.append(myDict[var])
            # print "myDict[var] is: ", myDict[var]
            utilVarKey = delComma(utilVarEvent)     #transfer list to tuple
            # print "utilVarKey: ", utilVarKey
        res += prob * utilInfo[utilVarKey]
        # print "res is: ", res
    return res

f = open(filename)

class Query():
    def __init__(self, title, variables, evidences, varnames):    #char e.g. 'P', dict e.g. Demoralize: +, dict e.g. LeakIdea: +, Infiltration: +
        self.title = title
        self.variables = variables    
        self.evidences = evidences
        self.varnames = varnames    # a list of variable names
    
    def numOfEU(self):  #useful only for MEU
        return len(self.varnames)

class BayesNode():
#Z = BayesNode('Z', 'P Q',  {(T, T): 0.2, (T, F): 0.3, (F, T): 0.5, (F, F): 0.7})
    def __init__(self, variables, parents, cpt):    #string, list, dict
        self.variables = variables    
        self.parents = parents
        self.cpt = cpt

class UtilityNode():
    def __init__(self, varnames, util):     #list, dict
        self.varnames = varnames
        self.util = util


bayesnet = {}
queries = []
#--- Construct Query instances ---#
while True:
    query = f.readline()
    if "*" in query:
        break
    variables = {}
    evidences = {}
    temp = query[query.find("(") + 1: query.find(")")].split(' | ')

    if len(temp) == 1:    # non-conditional probability. joint instead. No vars, only evidences
        varnamesM = []
        queryes = temp[0].split(', ')    # queryvars is a list
        for i in range(len(queryes)):
            if query[0] == 'M':
                varnamesM.append(queryes[i])      #queryes contains only variable names
            else:
                queryes_name = queryes[i].split(' = ')[0]
                queryes_occur = queryes[i].split(' = ')[1]
                queryes_occur = True if queryes_occur is '+' else False
                evidences.update({queryes_name:queryes_occur})
        #print "evidences:" , evidences
        onequery = Query(query[0], {}, evidences, varnamesM)
        queries.append(onequery)

    if len(temp) == 2:
        queryvars = temp[0].split(', ')    # queryvars is a list
        var_names = []
        for i in range(len(queryvars)):
            if query[0] == 'M':
                variables.update({queryvars[i]:True})
                var_names.append(queryvars[i])
            else:
                queryvars_name = queryvars[i].split(' = ')[0]
                var_names.append(queryvars_name)
                queryvars_occur = queryvars[i].split(' = ')[1]
                queryvars_occur = True if queryvars_occur is '+' else False
                variables.update({queryvars_name:queryvars_occur})
        #print "variables:", variables
        queryes = temp[1].split(', ')    # queryvars is a list
        for i in range(len(queryes)):
            queryes_name = queryes[i].split(' = ')[0]
            queryes_occur = queryes[i].split(' = ')[1]
            queryes_occur = True if queryes_occur is '+' else False
            evidences.update({queryes_name:queryes_occur})
        #print "evidences:" , evidences
        onequery = Query(query[0], variables, evidences, var_names)
        queries.append(onequery)
        #print "variables:", variables
        #print "varnames:", var_names
cntLines = len(queries)
'''
for i in range(len(queries)):
    
    print "test query instances"
    print queries[i].title
    print queries[i].variables
    print queries[i].evidences
    print queries[i].varnames
    '''

#--- Construct Node instances ---#
global_var = []
global_utilinfo = {}
bnvars = []
done = 0
while not done:
    sentence = f.readline().strip()
    if "*" in sentence:
        continue

    if sentence == '':
        done = 1
        continue
    
    if sentence[0].isupper():    # variable1 | parent01, parent02...
        temp = sentence.split(' | ')
        cptvar = temp[0]   # a string
        bnvars.append(cptvar)
        cptpars = []
        cptinfo = {}
        # print "len of cptpars:", len(cptpars)
        if len(temp) == 2:
            cptpars = temp[1].split(' ')   # a list
        for i in range(2**len(cptpars)):
            oneprob = f.readline().strip().split(' ')
            #print oneprob
            if oneprob[0] == 'decision':
                del bnvars[len(bnvars)-1]
                break
            for j in range(len(oneprob)):
                con_prob = float(oneprob[0])
                con_occur = oneprob[1:]
                for k in range(len(con_occur)):
                    con_occur[k] = True if con_occur[k] is "+" else False
                con_occur = delComma(con_occur)
                cptinfo.update({con_occur:con_prob})
        onenode = BayesNode(cptvar, cptpars, cptinfo)
        bayesnet[cptvar] = (onenode)

    if sentence[0] == 'u':      #utility node
        utilinfo = {}
        global_var = sentence.split(' | ')[1].split(' ')
        for i in range(2**len(global_var)):
            oneutil = f.readline().strip().split(' ')
            for j in range(len(oneutil)):
                utilNum = float(oneutil[0])
                utilEvent = oneutil[1:]
                for k in range(len(utilEvent)):
                    utilEvent[k] = True if utilEvent[k] is "+" else False
                utilEvent = delComma(utilEvent)
                global_utilinfo.update({utilEvent:utilNum})
utilNode = UtilityNode(global_var, global_utilinfo)

f.close()
'''
print "TEST INPUT AAAAAGAIN"
print bayesnet["NightDefense"].variables
print bayesnet["NightDefense"].parents
print bayesnet["NightDefense"].cpt
'''
f1 = open('output.txt', 'w')
for i in range(len(queries)):
    '''
    print "TEST INPUT"
    print "query_title:", queries[i].title
    print "query_vars:", queries[i].variables
    print "query_evi:", queries[i].evidences
    print "queries[i].var_names:", queries[i].varnames
    print "END TEST"
    '''
    if queries[i].title == 'P':
        normalizedQ = enumeration_ask(queries[i].varnames, queries[i].evidences, bnvars)
        keyName = event_values(queries[i].variables, queries[i].varnames)
        #--- round function ---#
        a = normalizedQ[keyName]
        res = Decimal(str(a)).quantize(Decimal('.01'))
        #print "Final answer:", res
        f1.write(str(res))
        cntLines -= 1
        if cntLines != 0:
            f1.write("\n")

    if queries[i].title == 'E':
        keyEvents = {}
        p_varnames = queries[i].varnames
        p_evidences = queries[i].evidences
        utilVar = utilNode.varnames
        if not queries[i].varnames:    # no | in EU
            for j in range(len(utilVar)):
                if utilVar[j] not in queries[i].evidences:
                    p_varnames.append(utilVar[j])
                else:
                    keyEvents[utilVar[j]] = queries[i].evidences[utilVar[j]]
            # print "TEST keyEvents"
            # print keyEvents
        else:
            for j in range(len(utilVar)):
                if utilVar[j] not in queries[i].varnames:
                    p_varnames.append(utilVar[j])
                else:   # overlap between utility node and EU variables
                    p_varnames.remove(utilVar[j])
                    keyEvents[utilVar[j]] = queries[i].variables[utilVar[j]]
            # print "TEST keyEvents"
            # print keyEvents
            for varname in p_varnames:
                #print p_varnames
                if varname not in utilVar:
                    toBeRemoved = varname
                    p_varnames.remove(toBeRemoved)
                    #print "Removed:", toBeRemoved
                    p_evidences.update({toBeRemoved:queries[i].variables[toBeRemoved]})
        
        
        normalizedQ = enumeration_ask(p_varnames, p_evidences, bnvars)
        #print normalizedQ

        euVal = utility(utilNode.util, utilNode.varnames, normalizedQ, p_varnames, keyEvents)
        a = euVal
        res = Decimal(str(a)).quantize(Decimal('0'))
        #print "final EU: ", res
        f1.write(str(res))
        cntLines -= 1
        if cntLines != 0:
            f1.write("\n")

    if queries[i].title == 'M':
        allEU = []
        maxEU = None    #min value
        opt = []
        '''
        print 'TEST MEU:'
        print queries[i].varnames
        print queries[i].variables
        print queries[i].evidences

        print "END MEU"
        '''
        
        for oneEvent in createTrueFalse(len(queries[i].varnames)):
            # print "TEST MEU"

            newEvent = mergeToDict(queries[i].varnames, oneEvent)
            #print "oneEvent: ", newEvent
            keyEvents = {}
            eu_varnames = [] if not queries[i].evidences else copy.deepcopy(queries[i].varnames)
            eu_variables = {} if not queries[i].evidences else newEvent
            eu_evidences = newEvent if not queries[i].evidences else copy.deepcopy(queries[i].evidences)
            p_varnames = eu_varnames
            p_evidences = eu_evidences
            utilVar = utilNode.varnames
            if not eu_varnames:    # no | in EU
                for j in range(len(utilVar)):
                    if utilVar[j] not in eu_evidences:
                        p_varnames.append(utilVar[j])
                    else:
                        keyEvents[utilVar[j]] = eu_evidences[utilVar[j]]
                # print "TEST keyEvents"
                # print keyEvents
            else:
                for j in range(len(utilVar)):
                    if utilVar[j] not in eu_varnames:
                        p_varnames.append(utilVar[j])
                    else:   # overlap between utility node and EU variables
                        p_varnames.remove(utilVar[j])
                        keyEvents[utilVar[j]] = eu_variables[utilVar[j]]
                # print "TEST keyEvents"
                # print keyEvents
                for varname in p_varnames:
                    #print p_varnames
                    if varname not in utilVar:
                        toBeRemoved = varname
                        p_varnames.remove(toBeRemoved)
                        #print "Removed:", toBeRemoved
                        p_evidences.update({toBeRemoved:eu_variables[toBeRemoved]})
            #print "p_varnames: ", p_varnames
            #print "p_evidences: ",p_evidences
            
            normalizedQ = enumeration_ask(p_varnames, p_evidences, bnvars)
            #print normalizedQ

            euVal = utility(utilNode.util, utilNode.varnames, normalizedQ, p_varnames, keyEvents)
            #print "EU: ", euVal

            if euVal > maxEU:
                maxEU = euVal
                opt = oneEvent
        a = maxEU
        meuVal = Decimal(str(a)).quantize(Decimal('0'))
        meuRes = []
        for var in opt:
            temp = '+' if var else '-'
            f1.write(temp + ' ')
        f1.write(str(meuVal))
        cntLines -= 1
        if cntLines != 0:
            f1.write("\n")
f1.close()




