
__author__="Chamara"
__date__ ="$Apr 3, 2012 4:47:52 PM$"
from SimPy.Simulation import *
from random import Random,expovariate
import Queue

class Global_var:
    rand=Random(65432)
    processorCores = Resource(1) #number of cores 1

class Arrival(Process):
    packetID = 0
    qLengthBytes = 0
    WaitMonitor = Monitor()
    qSizeMon = Monitor()
    contentInSystem = Monitor()
    queueSize = 0
    SystemSize = 0
    contentQueue = Queue.Queue(0)
    def __init__(self,ArrTime,type,size):
        Process.__init__(self)
        self.ID = Arrival.packetID
        self.arrivalTime = ArrTime
        self.contentType = type
        self.size = size
        self.exitTime = 0
    def run(self):
        while 1:
            yield hold,self,self.arrivalTime
            content = Content(self.contentType,self.size,Arrival.packetID)
            Arrival.packetID+=1
            activate(content,content.run())
            # generate the next content size, type and arrival time
            self.arrivalTime = Global_var.rand.expovariate(2) # substitute with the actual function
            #self.size =
            #self.contentType=







class Content(Process):
    def __init__(self,type,size,id):
        Process.__init__(self)
        self.type = type
        self.size = size
        self.arrTime = now()
        self.id = id
        self.isQueued = 0
    def run(self):
        Arrival.SystemSize += self.size
        Arrival.contentInSystem.observe(Arrival.SystemSize)
        #get the service time of the current content
        serviceTime = Global_var.rand.expovariate(3) # substitute with the actual function
        if Global_var.processorCores.n == 1:
            Arrival.queueSize += self.size
            Arrival.qSizeMon.observe(Arrival.queueSize)
            self.isQueued = 1

        yield request,self,Global_var.processorCores
        #print 'ID of Content in service : '
        #print self.id
        yield hold,self,serviceTime
        Arrival.SystemSize -= self.size
        Arrival.contentInSystem.observe(Arrival.SystemSize)
        if self.isQueued ==1:
            Arrival.queueSize -= self.size
            Arrival.qSizeMon.observe(Arrival.queueSize)
        
        Arrival.qSizeMon.observe(Arrival.queueSize)
        Arrival.WaitMonitor.observe(now()-self.arrTime)
        yield release,self,Global_var.processorCores



def main():
    initialize()
    arrtime=Global_var.rand.expovariate(2)
    print arrtime
    #size =
    #contentType=
    arrProcess = Arrival(arrtime,'text',1)
    activate(arrProcess,arrProcess.run())
    simulate(until=10000)
    print 'Mean content Size in queue: '
    print Arrival.qSizeMon.timeAverage()
    print 'Mean content Size in System:'
    print Arrival.contentInSystem.timeAverage()
    print 'Average Wait:'
    print Arrival.WaitMonitor.mean()

if __name__ == "__main__": main()
    

