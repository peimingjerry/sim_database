
from util import *

############################
class netDefn:
    def __init__(self, name, scope):
        self.name = name
        self.scope = scope

############################       
class instDefn:
    def __init__(self, name, sdbInst):
        self.name = name
        self.parent = None
        self.master= None
        self.sdbObj = sdbInst
        self.nodes = list()
        self.is_hier = (self.sdbObj.getType() == 'Subckt')

    def setMaster(self, master):
        self.master = master

    def getMaster(self):
        return self.master

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent
              
    def addNode(self, node):
        self.nodes.append(node)

    def getNodes(self):
        return self.nodes
    
    def getNode(self,i):
        return self.nodes[i]

    def getNodeCount(self):
        return len(self.nodes)

    def isHier(self):
        return self.is_hier

    def getParams(self):
        if self.sdbObj:
            return self.sdbObj.params
        else:
            return None

    def findParam(self, paramName):
        if self.sdbObj:
            return self.sdbObj.findParam(paramName)
        return None
        
    def dump(self, level):
        offset = getDumpOffset(level)
        master_str = ''
        if self.master != None:
            master_str = self.master.name   
        inst_str = self.name+' ( '
        for node in self.nodes:
            inst_str += node.name + ' '
        param_str = ''
        for param in self.getParams():
            if param.isRefValue():
                value_str = param.getRefVar()
            else:
                value_str = str(param.getValue())
            param_str += param.name + '=' + value_str + ' '
        inst_str += ') ' + master_str + ' '+param_str
        print offset+inst_str
    
############################
class modelDefn:
    def __init__(self,name, sdbModel):
        self.name = name
        self.parent = None
        self.sdbObj = sdbModel
        self.prim = sdbModel.prim

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def getParams(self):
        if self.sdbObj:
            return self.sdbObj.params
        else:
            return None

    def findParam(self, paramName):
        if self.sdbObj:
            return self.sdbObj.findParam(paramName)
        return None
    
    def dump(self, level):
        offset = getDumpOffset(level)
        param_str = ''
        for param in self.getParams():
            if param.isRefValue():
                value_str = param.getRefVar()
            else:
                value_str = str(param.getValue())
            param_str += param.name + '=' + value_str + ' '
        print offset+'model ',self.name,' ', self.prim, ' ', param_str
    
############################
class subcktDefn:
    def __init__(self,name,sdbSubckt):
        self.name = name
        self.parent = None
        self.sdbObj = sdbSubckt
        self.terms = list()
        self.nodes = list()
        self.insts = list()
        self.models = list()
        self.subckts = list()

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent
                
    def addInstance(self, inst):
        self.insts.append(inst)

    def getInstances(self):
        return self.insts

    def addModel(self, model):
        self.models.append(model)

    def getModels(self):
        return self.models

    def addSubckt(self, subckt):
        self.subckts.append(subckt)

    def getSubckts(self):
        return self.subckts
    
    def addTerm(self, term):
        self.terms.append(term)

    def getTerms(self):
        return self.terms
    
    def getTerm(self,i):
        return self.terms[i]

    def getTermCount(self):
        return len(self.terms)
    
    def addNode(self, node):
        self.nodes.append(node)

    def getNodes(self):
        return self.nodes
    
    def getNode(self,i):
        return self.nodes[i]

    def getNodeCount(self):
        return len(self.nodes)

    def findSubckt(self, subcktName):
        foundMaster = None
        for subckt in self.getSubckts():
            if subcktName == subckt.name:
                foundMaster = subckt
                break
        return foundMaster

    def findModel(self, modelName):
        foundMaster = None
        for model in self.getModels():
            if modelName == model.name:
                foundMaster = model
                break
        return foundMaster

    def getParams(self):
        if self.sdbObj:
            return self.sdbObj.params
        else:
            return None

    def findParam(self, paramName):
        if self.sdbObj:
            return self.sdbObj.findParam(paramName)
        return None
    
    def dump(self, level):
        offset = getDumpOffset(level)
        term_str = ''
        for term in self.terms:
            term_str += term.name + ' '
        title_str = offset+'subckt '+self.name+' ( '+term_str+')'
        print offset + title_str
        self.dump_content(level+1)
        print offset + 'ends'
        
    def dump_content(self, level):
        offset = getDumpOffset(level)
        node_str = 'local nodes { '
        for node in self.nodes:
            node_str += node.name + ' '
        node_str += '}'
        print offset + node_str
        
        param_str = ''
        for param in self.getParams():
            if param.isRefValue():
                value_str = param.getRefVar()
            else:
                value_str = str(param.getValue())
            param_str += param.name + '=' + value_str + ' '
        print offset + 'parameters ' + param_str
        
        for model in self.models:
            model.dump(level)
        for subckt in self.subckts:
            subckt.dump(level)
        for inst in self.insts:
            inst.dump(level)
            
class circuitDefn(subcktDefn):
    def __init__(self, sdb_ckt):
        subcktDefn.__init__(self, None, sdb_ckt)
        
    def dump(self):
        subcktDefn.dump_content(self, 0)
        
    
############################
def getSubcktDDB(sdb_subckt, subckt_defn):    
    'create model defn'
    for model in sdb_subckt.getModels():
        model_defn = modelDefn(model.name, model)
        model_defn.setParent(subckt_defn)
        subckt_defn.addModel(model_defn)

    'create terminals'
    for term in sdb_subckt.getTerms():
        subckt_defn.addTerm(netDefn(term, 'scopeTerm'))

    'create nested subckts'
    for subckt in sdb_subckt.getSubckts():
        sub_subckt_defn = subcktDefn(subckt.name, subckt)
        sub_subckt_defn.setParent(subckt_defn)
        getSubcktDDB(subckt, sub_subckt_defn)
        subckt_defn.addSubckt(sub_subckt_defn)

    'create instances'
    for inst in sdb_subckt.getInstances():
        inst_defn = instDefn(inst.name, inst)
        inst_defn.setParent(subckt_defn)
        
        'bind instances'
        foundMaster = None
        if inst.getType() == 'Subckt':
            foundMaster = subckt_defn.findSubckt(inst.getMaster())
            if foundMaster == None:
                tmpInst = inst_defn.getParent()
                while tmpInst != None:
                    foundMaster = tmpInst.findSubckt(inst.getMaster())
                    if foundMaster != None:
                        break
                    tmpInst = tmpInst.getParent()
            if foundMaster != None:
                inst_defn.setMaster(foundMaster)
            else:
                print 'Cannot find subckt definition for ',inst.name,' with name ',inst.getMaster()
        elif inst.getType() == 'Resistor':
            foundMaster = subckt_defn.findModel(inst.getMaster())
            if foundMaster == None:
                tmpInst = inst_defn.getParent()
                while tmpInst != None:
                    foundMaster = tmpInst.findModel(inst.getMaster())
                    if foundMaster != None:
                        break
                    tmpInst = tmpInst.getParent()
            if foundMaster != None:
                inst_defn.setMaster(foundMaster)
            else:
                print 'Cannot find model definition for ',inst.name,' with name ',inst.getMaster()

        'create nodes'
        for node in inst.nodes:
            foundTerm = None
            for term in subckt_defn.getTerms():
                if node == term.name:
                    foundTerm = term
                    break
            if foundTerm != None:
                inst_defn.addNode(foundTerm)
            else:
                foundNode = None
                for i in subckt_defn.nodes:
                    if node == i.name:
                        foundNode = i
                        break
                if foundNode != None:
                    inst_defn.addNode(foundNode)
                else:
                    newNode = netDefn(node,'scopeLocal')
                    inst_defn.addNode(newNode)
                    subckt_defn.addNode(newNode)
        subckt_defn.addInstance(inst_defn)
        
############################
def getDDB(sdb_ckt):
    ckt_defn = circuitDefn(sdb_ckt)
    getSubcktDDB(sdb_ckt, ckt_defn)
    return ckt_defn

