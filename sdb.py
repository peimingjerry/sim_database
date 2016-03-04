
class visitor:
    def __init__(self):
        print 'this is a visitor: ', self.__doc__
        
class dumpInstancesVisitor(visitor):
    'visitor to dump instances'
    def action(self, instance):
        print 'Visiting: ',instance.name
        print '  instances:'
        for i in instance.instances:
            print '    ', i.name
            
class dumpNodesVisitor(visitor):
    'visitor to dump nodes'
    def action(self, instance):
        print 'Visiting: ',instance.name
        print '  nodes:'
        for i in instance.nodes:
            print '    ', i

class instance:
    def __init__(self, name=None):
        self.nodes = list()
        self.instances = list()
        self.name = name

    def addNode(self, node):
        self.nodes.append(node)

    def addInstance(self, instance):
        self.instances.append(instance)

    def acceptVisitor(self, visitor):
        visitor.action(self)
        for eachInst in self.instances:
            visitor.action(eachInst)

def main():
def getSDB():
    ''' the input is:
       subckt sub1 1 2
       r1 1 2 r=r
       ends
       subckt sub2 1 2
       r2 1 2
       ends
       x1 n1 n2 sub1 r=1
       x2 n2 n3 sub1 r=2
       x3 n3 n4 sub2
       r3 n1 n4 r=3
'''
    sdbDesign = sdbContex()
    
    sub1 = sdbSubckt('sub1')
    sub1.addTerm('1')
    sub1.addTerm('2')
    sub1.addParam('r')
    r1 = sdbInst('r1')
    r1.addTerm('1')
    r1.addNode('2')
    r1.addNode('r')
    r1.setMaster('resistor')
    sub1.addInst(r1)

    sub2 = sdbSubckt('sub2')
    sub2.addTerm('1')
    sub2.addTerm('2')
    r2 = sdbInst('r2')
    r2.addNode('1')
    r2.addNode('2')
    r2.setMaster('resistor')
    sub2.addInst(r2)

    x1 = sdbInst('x1')
    x1.addNode('n1')
    x1.addNode('n2')
    x1.setMaster('sub1')
    x1.addParam('r',1)
    
    x2 = sdbInst('x2')
    x2.addNode('n2')
    x2.addNode('n3')
    x2.setMaster('sub1')
    x2.addParam('r',2)

    x3 = sdbInst('x3')
    x3.addNode('n3')
    x3.addNode('n4')
    x3.setMaster('sub2')

    r3 = sdbInst('r3')
    r3.setMaster('resistor')
    r3.addNode('n1')
    r3.addNode('n4')
    r3.addParam('r',3)

    sdbDesign.addNode('n1')
    sdbDesign.addNode('n2')
    sdbDesign.addNode('n3')
    sdbDesign.addNode('n4')
    
    sdbDesign.addInst('x1')
    sdbDesign.addInst('x2')
    sdbDesign.addInst('x3')
    sdbDesign.addInst('r3')

    sdbDesign.addModel('sub1')
    sdbDesign.addModel('sub2')
    sdbDesign.addModel('resistor')

    return sdbDesign
    
    for i in range(2)
        1
    
    topInst = instance()
    for i in range(4):
        topInst.addNode(str('n%d'%i))

    for i in range(3):
        subInst = instance(str('i%d'%i))
        topInst.addInstance(subInst)
        for j in range(2):
            subInst.addNode(str('n_%d_%d'%(i,j)))

    topInst.acceptVisitor( dumpNodesVisitor() )
    topInst.acceptVisitor( dumpInstancesVisitor() )


if __name__ == '__main__':
    main()
