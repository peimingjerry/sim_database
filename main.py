
from sdb import *
from ddb import *
from edb import *

############################
def main():
    print '\nSDB:'
    sdbCkt = getSDB()
    #sdbCkt.dump()

    print '\nDDB:'
    ddbCkt = getDDB(sdbCkt)
    ddbCkt.dump()

    print '\nEDB:'
    edbCkt = getEDB(ddbCkt)
    edbCkt.dump()

############################
if __name__ == '__main__':
    main()
