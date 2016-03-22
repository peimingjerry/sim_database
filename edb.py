
from util import *

############################
class paramExt:
    def __init__(self, name):
        self.name = name
        self.evaluated = False

    def setValue(self, value):
        self.value = value
        self.evaluated = True

    def getValue(self):
        if self.evaluated:
            return self.value
        else:
            return None

    def isEvaluated(self):
        return self.evaluated
    
############################
class netExt:
    def __init__(self, netDefn):
        self.netDefn = netDefn
        self.isAlias = False
        self.actualNode = None

    def getName(self):
        if self.netDefn:
            return self.netDefn.name
        else:
            return None
        
    def setActualNode(self, actualNetDefn):
        self.actualNode = actualNetDefn
        self.isAlias = True

    def isAliasNode(self):
        return self.isAlias
    
    def getActualNode(self):
        return self.actualNode
    
############################
class masterExt:
    def __init__(self, name):
        self.name = name

    def setMasterDefn(self, masterDefn):
        self.masterDefn = masterDefn

    def getMasterDefn(self):
        return self.masterDefn
        
############################       
class instExt:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.master= None
        self.defn = None
        self.terms = list()
        self.isHier = False
        self.params = list()

    def setIsHier(self, isHier):
        self.isHier = isHier

    def getIsHier(self):
        return self.isHier
    
    def setMaster(self, master):
        self.master = master

    def getMaster(self):
        return self.master

    def setInstDefn(self, defn):
        self.defn = defn

    def getInstDefn(self):
        return self.defn
    
    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def addTerm(self, term):
        self.terms.append(term)

    def getTerms(self):
        return self.terms
    
    def getTerm(self,i):
        return self.terms[i]

    def getTermCount(self):
        return len(self.terms)

    def addParam(self, param):
        self.params.append(param)

    def getParams(self):
        return self.params

    def findParam(self, paramName):
        for p in self.params:
            if p.name == paramName:
                return p
        return None
    
    def dump(self, level):
        offset = getDumpOffset(level)
        master_str = ''
        if self.master != None:
            master_str = self.master.name   
        inst_str = self.name+' ( '
        for term in self.terms:
            inst_str += term.getName() + ' '
        param_str = ''
        for param in self.getParams():
            value_str = ''
            if param.isEvaluated():
                value_str = str(param.getValue())
            param_str += param.name + '=' + value_str + ' '
        inst_str += ') ' + master_str + ' ' + param_str
        print offset+inst_str
        
############################
class subcktInstExt(instExt):
    def __init__(self, name):
        instExt.__init__(self, name)
        instExt.setIsHier(self, True)
        self.insts = list()
        self.nodes = list()
        self.params = list()
        
    def addNode(self, node):
        self.nodes.append(node)

    def getNodes(self):
        return self.nodes
    
    def getNode(self,i):
        return self.nodes[i]

    def getNodeCount(self):
        return len(self.nodes)

    def addInstance(self, inst):
        self.insts.append(inst)

    def getInstances(self):
        return self.insts

    def addParam(self, param):
        self.params.append(param)

    def getParams(self):
        return self.params

    def findParam(self, paramName):
        for p in self.params:
            if p.name == paramName:
                return p
        return None
    
    def dump(self, level):
        offset = getDumpOffset(level)
        term_str = ''
        for term in self.terms:
            actual_node_name = ''
            if term.isAliasNode():
                actual_node_name = term.getActualNode().name
            term_str += term.getName() + ':'+actual_node_name + ' '
        title_str = self.name+' ( '+term_str+')' +self.getMaster().name
        param_str = ''
        for param in self.getParams():
            value_str = ''
            if param.isEvaluated():
                value_str = str(param.getValue())
            param_str += param.name + '=' + value_str + ' '
        if printDebug:
            print offset + title_str + ' ' + param_str
        else:
            print offset + title_str
        self.dump_content(level+1)
        
    def dump_content(self, level):
        offset = getDumpOffset(level)
        node_str = 'local nodes { '
        for node in self.nodes:
            node_str += node.name + ' '
        node_str += '}'
        print offset + node_str
        #for model in self.models:
        #    model.dump(level)
        for inst in self.getInstances():
            inst.dump(level)
            
class circuitInstExt(subcktInstExt):
    def __init__(self):
        subcktInstExt.__init__(self, None)
        
    def dump(self):
        subcktInstExt.dump_content(self, 0)
        
############################
def getSubcktEDB(subckt_defn, subckt_inst_ext):
    for node in subckt_defn.getNodes():
        subckt_inst_ext.addNode(node)
        
    for inst in subckt_defn.getInstances():
        master_defn = inst.getMaster()
        #subckt_inst_ext.addMaster(master_defn)
        master_ext = masterExt(master_defn.name)
        master_ext.setMasterDefn(master_defn)        
        if inst.isHier():
            inst_ext = subcktInstExt(inst.name)
        else:
            inst_ext = instExt(inst.name) 
        inst_ext.setParent(subckt_inst_ext)
        inst_ext.setInstDefn(inst)
        inst_ext.setMaster(master_ext)
        subckt_inst_ext.addInstance(inst_ext)

        'deal with set parameters'
        for param in inst.getParams():
            if inst.isHier() and master_defn.findParam(param.name) == None:
                continue
            param_ext = paramExt(param.name)
            if param.isRefValue():
                param_value = param.getRefVar()
                foundParam = inst_ext.getParent().findParam(param_value)
                if foundParam == None:
                    print 'Cannot set parameter value of ',param.name,' for instance ',inst.name
                else:
                    assert(foundParam.isEvaluated())
                    param_ext.setValue(foundParam.getValue())
            else:
                param_ext.setValue(param.getValue())
            inst_ext.addParam(param_ext)
            
        'deal with subckt default parameters'
        if inst.isHier():
            for param in master_defn.getParams():
                foundParam = inst_ext.findParam(param.name)
                if foundParam == None:
                    param_ext = paramExt(param.name)
                    if not param.isRefValue():
                        param_ext.setValue(param.getValue())
                        inst_ext.addParam(param_ext)
            
        if inst.isHier():
            assert(master_defn.getTermCount() == inst.getNodeCount())
            for i in range(master_defn.getTermCount()):
                net = netExt(master_defn.getTerm(i))
                net.setActualNode(inst.getNode(i))
                inst_ext.addTerm(net)
            getSubcktEDB(master_defn, inst_ext)
        else:      
            for node in inst.nodes:
                net = netExt(node)
                inst_ext.addTerm(net)
    
############################
def getEDB(ddbCkt):
    edbCkt = circuitInstExt()
    getSubcktEDB(ddbCkt, edbCkt)
    return edbCkt
