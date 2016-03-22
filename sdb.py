
from util import *

############################
class sdbParam:
    def __init__(self, name):
        self.name = name
        self.valueType = 'Value'
        self.refVar = None
        self.value = None

    def setValue(self, value):
        self.value = value
        self.valueType = 'Value'

    def getValue(self):
        return self.value

    def setRefVar(self, var):
        self.refVar = var
        self.valueType = 'RefVar'

    def getRefVar(self):
        return self.refVar

    def isRefValue(self):
        return (self.valueType == 'RefVar')

############################
class sdbInst:
    def __init__(self, name):
        self.name = name
        self.nodes = list()
        self.params = list()

    def addParam(self, param):
        self.params.append(param)

    def getParams(self):
        return self.params

    def findParam(self, paramName):
        for p in self.params:
            if p.name == paramName:
                return p
        return None
    
    def setMaster(self, master):
        self.master = master

    def getMaster(self):
        return self.master

    def setType(self, mtype):
        self.type = mtype

    def getType(self):
        return self.type

    def addNode(self, node):
        self.nodes.append(node)

    def getNodes(self):
        return self.nodes
    
    def getNode(self,i):
        return self.nodes[i]

    def getNodeCount(self):
        return len(self.nodes)

    def dump(self, level):
        offset = getDumpOffset(level)
        print offset,'<inst name=',self.name,' mtype=',self.type,' master=', self.master,'/>'
        for param in self.params:
            if param.isRefValue():
                value_str = param.getRefVar()
            else:
                value_str = str(param.getValue())
            print offset,'    <param name=',param.name,' value=',value_str,'/>'
        for node in self.nodes:
            print offset, '    <node name=', node, '/>'
        print offset,'</inst>'

############################
class sdbModel:
    def __init__(self, name):
        self.name = name
        self.params = list()

    def addParam(self, param):
        self.params.append(param)

    def getParams(self):
        return self.params

    def findParam(self, paramName):
        for p in self.params:
            if p.name == paramName:
                return p
        return None
    
    def setPrimitive(self, prim):
        self.prim = prim

    def dump(self, level):
        offset = getDumpOffset(level)
        print offset,'<model name=',self.name,' primitive=', self.prim,'>'
        for param in self.params:
            if param.isRefValue():
                value_str = param.getRefVar()
            else:
                value_str = str(param.getValue())
            print offset,'    <param name=',param.name,' value=',value_str,'/>'
        print offset,'</model>'
        
############################
class sdbSubckt:
    def __init__(self, name):
        self.name = name
        self.params = list()
        self.insts = list()
        self.models = list()
        self.subckts = list()
        self.terms = list()
        self.nodes = list()

    def addParam(self, param):
        self.params.append(param)

    def getParams(self):
        return self.params

    def findParam(self, paramName):
        for p in self.params:
            if p.name == paramName:
                return p
        return None
    
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
    
    def dump(self, level):
        offset = getDumpOffset(level)
        print offset,'<subckt name=',self.name,'>'
        self.dump_content(level+1)
        print offset,'</subckt>'

    def dump_content(self, level):
        offset = getDumpOffset(level)
        for term in self.terms:
            print offset, '<term name=', term, '/>'
        for param in self.params:
            if param.isRefValue():
                value_str = param.getRefVar()
            else:
                value_str = str(param.getValue())
            print offset,'<param name=',param.name,' value=',value_str,'/>'
        for model in self.models:
            model.dump(level)
        for subckt in self.subckts:
            subckt.dump(level)
        for inst in self.insts:
            inst.dump(level)

            
############################
class sdbCircuit(sdbSubckt):
    def __init__(self):
        #super(sdbCircuit, self).__init__('')
        sdbSubckt.__init__(self, None)

    def dump(self):
        sdbSubckt.dump_content(self, 0)        
        
############################
def getSDB():
    sdbCkt = sdbCircuit()
    myRes = sdbModel('myRes')
    myRes.setPrimitive('resistor')
    sdbCkt.addModel(myRes)

    sub1 = sdbSubckt('sub1')
    sub1.addTerm('1')
    sub1.addTerm('2')
    sub1_param_1 = sdbParam('r')
    sub1_param_1.setValue(100)
    sub1.addParam(sub1_param_1)
    sub1_param_2 = sdbParam('tc1')
    sub1_param_2.setValue(1)
    sub1.addParam(sub1_param_2)
    r1 = sdbInst('r1')
    r1.setType('Resistor')
    r1.setMaster('myRes')
    r1.addNode('1')
    r1.addNode('2')
    r1_param_1 = sdbParam('r')
    r1_param_1.setRefVar('r')
    r1.addParam(r1_param_1)
    r1_param_2 = sdbParam('tc1')
    r1_param_2.setRefVar('tc1')
    r1.addParam(r1_param_2)
    sub1.addInstance(r1)
    sdbCkt.addSubckt(sub1)

    sub2 = sdbSubckt('sub2')
    sub2.addTerm('1')
    sub2.addTerm('2')
    sub2_param_1 = sdbParam('r')
    sub2_param_1.setValue(100)
    sub2.addParam(sub2_param_1)
    sub2_param_2 = sdbParam('tc1')
    sub2_param_2.setValue(1)
    sub2.addParam(sub2_param_2)
    r2 = sdbInst('r2')
    r2.setType('Resistor')
    r2.setMaster('myRes')
    r2.addNode('1')
    r2.addNode('2')
    r2_param = sdbParam('r')
    r2_param.setRefVar('r')
    r2.addParam(r2_param)
    sub2.addInstance(r2)
    x21 = sdbInst('x21')
    x21.setType('Subckt')
    x21.setMaster('sub1')
    x21.addNode('1')
    x21.addNode('2')
    x21_param_1 = sdbParam('r')
    x21_param_1.setRefVar('r')
    x21.addParam(x21_param_1)
    x21_param_2 = sdbParam('tc1')
    x21_param_2.setRefVar('tc1')
    x21.addParam(x21_param_2)
    sub2.addInstance(x21)
    sdbCkt.addSubckt(sub2)
    
    x1 = sdbInst('x1')
    x1.setType('Subckt')
    x1.setMaster('sub1')
    x1.addNode('n1')
    x1.addNode('n2')
    sdbCkt.addInstance(x1)
    
    x2 = sdbInst('x2')
    x2.setType('Subckt')
    x2.setMaster('sub1')
    x2.addNode('n2')
    x2.addNode('n3')
    x2_param_1 = sdbParam('r')
    x2_param_1.setValue(2)
    x2.addParam(x2_param_1)
    sdbCkt.addInstance(x2)
    
    x3 = sdbInst('x3')
    x3.setType('Subckt')
    x3.setMaster('sub2')
    x3.addNode('n3')
    x3.addNode('n4')
    x3_param_1 = sdbParam('r')
    x3_param_1.setValue(3)
    x3.addParam(x3_param_1)
    x3_param_2 = sdbParam('tc1')
    x3_param_2.setValue(3)
    x3.addParam(x3_param_2)
    x3_param_3 = sdbParam('tc2')
    x3_param_3.setValue(3)
    x3.addParam(x3_param_3)
    sdbCkt.addInstance(x3)
    
    r3 = sdbInst('r3')
    r3.setType('Resistor')
    r3.setMaster('myRes')
    r3.addNode('n1')
    r3.addNode('n4')
    r3_param_1 = sdbParam('r')
    r3_param_1.setValue(4)
    r3.addParam(r3_param_1)
    r3_param_2 = sdbParam('tc1')
    r3_param_2.setValue(1.0)
    r3.addParam(r3_param_2)
    r3_param_3 = sdbParam('tc2')
    r3_param_3.setValue(2.0)
    r3.addParam(r3_param_3)
    sdbCkt.addInstance(r3)
    
    return sdbCkt
