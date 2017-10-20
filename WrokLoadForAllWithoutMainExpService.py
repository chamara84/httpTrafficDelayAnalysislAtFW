

__author__="Chamara"
__date__ ="$Apr 21, 2012 11:56:18 AM$"



from SimPy.Simulation import *
#from SimPy.SimPlot import *
import Queue
import csv
import math
import numpy
from numpy import random
from scipy import stats
from scipy import constants
import string
#from decimal import *

class Global_var(object):
	
	def __init__(self):
		self.numberOfcores = 1
		#self.scale_par = scalePar
		#self.contentType = 'All'
		self.workload = list([0.0])
		self.rand = random.mtrand.RandomState()
		self.process = Simulation()
		self.queueLengthMon = Monitor(sim=self.process, name = 'Queue length')
		self.workLoadMon = Monitor(sim=self.process, name = 'Workload')
		self.waitTimeMon = Monitor(sim=self.process, name = 'Wait Time in System')
		self.processorCores = Resource(self.numberOfcores,sim=self.process,monitored=True, monitorType=Monitor) #number of cores
		self.queueLength = list([0])
		self.serviceTimesMon = list([])
		self.interArrivalTime = Tally(sim=self.process)
    	
class Arrival(Process):
    #packetID = 0
    
    def __init__(self,ArrTime,type,size,packetID,scale_par,globalVar,lines):
        Process.__init__(self ,sim = globalVar.process ,name = 'ArrProcess')
        self.ID = packetID
        self.scalepar = float(scale_par)
        self.arrTime =max(float(ArrTime),0.0)/self.scalepar 
        self.interArrivalTime = max(float(ArrTime),0.0)
        self.contentType = type
        
        try:
        	self.size = long(size)
        except:
			self.size = 0  
			    
        self.exitTime = 0
        #self.sim = sim
        #self.serviceProObj = ServiceProcess()
        #self.globalVar = Global_var(self.scale_par) 
        #self.serveTime = self.serviceProObj.serviceTime(self.contentType,self.size,globalVar)
        self.lines = numpy.array(lines)
        lines = []    
    
            
                
    def run(self,globalVar,meanService):
    	print str(len(self.lines))
    	self.serveTime = numpy.random.exponential(scale=meanService, size=None)
    	#self.interArrivalTimeVec = [(max(float(self.lines[index+1][0])-float(self.lines[index][0]),0.0)/float(self.scalepar)) for index in range(len(self.lines)-1)]
    	#self.interArrivalTimeVec.insert(0,float(self.arrTime))
        #self.interArrivalTimeVec = tuple(self.interArrivalTimeVec)
        #numpy.random.shuffle(self.interArrivalTimeVec)
    	#self.interArrivalTimeVec = self.returnModifVals(self.interArrivalTimeVec,[59.0/self.scalepar],['less'],'one') # function shuffles the values that is not in interval if last arg is 'one' else if 'both' shuffle each independently and merge
        
        while 1:
        	       	
        	yield hold,self,float(self.interArrivalTime)                #self.ArrTime
        	
        	if self.ID == len(self.lines) - 1:
        		print 'Last Arr at : '+str(globalVar.process.now()) 
        	if self.ID<len(self.lines):
        		globalVar.interArrivalTime.observe(float(self.interArrivalTime))
        		content = Content(self.size,self.contentType,self.serveTime,self.ID,len(self.lines),globalVar)
        		globalVar.process.activate(content,content.run(globalVar), at=globalVar.process.now())
        		self.ID = self.ID + 1
        		
        	# generate the next content size, type and arrival time
        	if self.ID<len(self.lines):
        		self.interArrivalTime = float(max(float(self.lines[self.ID][0])-float(self.lines[self.ID-1][0]),0.0))# substitute with the actual function
        		try:
        		 	self.size =  long(self.lines[self.ID][3])
        		except:
        		 	self.size=0
        		self.contentType=self.lines[self.ID][1]
        		self.serveTime = numpy.random.exponential(scale=meanService, size=None)
        		globalVar.serviceTimesMon.append(float(self.serveTime))

    
    def returnModifVals(self,values,boundry,inequality,shuffleWhat):
        
        self.valueTuple = []
        self.values = values
        self.unsatVal = []
        for index in range(len(self.values)):
            
            if len(inequality) == 1 and string.find(str(inequality[0]),str('less'))!= -1 and len(boundry) == 1:
                
                if self.values[index] <= float(boundry[0]):
                    self.valueTuple.append([index,self.values[index]])
                
                else:
                    self.unsatVal.append([index,self.values[index]])
                    continue
            
            
            
            elif len(inequality) == 1 and string.find(str(inequality[0]),str('greater'))!= -1 and len(boundry) == 1:
                
                if self.values[index] >= float(boundry[0]):
                    
                    self.valueTuple.append([index,self.values[index]])
                
                else:
                    self.unsatVal.append([index,self.values[index]])
                    continue
            
            elif len(inequality) == 1 and string.find(str(inequality[0]),str('inner'))!= -1 and len(boundry) == 2:
                
                if float(boundry[0])<=float(boundry[1]) and self.values[index] >= float(boundry[0]) and self.values[index] <= float(boundry[1]):
                    
                    self.valueTuple.append([index,self.values[index]])
                
                elif float(boundry[0])>float(boundry[1]) and self.values[index] <= float(boundry[0]) and self.values[index]>= float(boundry[1]):
                    
                    self.valueTuple.append([index,self.values[index]])
                
                else:
                    self.unsatVal.append([index,self.values[index]])
                    continue
            
            
            else:
                raise ValueError('Invalid Input')
        
        self.unsatVal = numpy.array(self.unsatVal)
        #print 'Size Unsat:'+ str(numpy.size(self.unsatVal,0))+str(numpy.size(self.unsatVal,1))
        #print 'Size value:'+ str(numpy.size(self.valueTuple,0))+str(numpy.size(self.valueTuple,1))
                    
        self.unsatValIndex, self.unsatValValues = numpy.hsplit(self.unsatVal,2)
        
        
        if string.find(str(shuffleWhat),str('one'))!= -1:
            self.unsatVal = [float(self.unsatValValues[index]) for index in range(len(self.unsatValValues))]
            numpy.random.shuffle(self.unsatVal)
            
            for value in self.valueTuple:
                self.unsatVal.insert(value[0],value[1])
            return self.values
        
        elif string.find(str(shuffleWhat),str('both'))!= -1:
            
            self.valueTuple = numpy.array(self.valueTuple)
            self.valueTupleIndex, self.valueTupleValues = numpy.hsplit(self.valueTuple,2)
            numpy.random.shuffle(self.valueTupleValues)
            self.valueTuple = numpy.hstack((self.valueTupleIndex,self.valueTupleValues))
            #print 'Rows,valueTuple : '+str(self.valueTuple[0]) 
            numpy.random.shuffle(self.unsatValValues)
            self.unsatVal = numpy.hstack((self.unsatValIndex,self.unsatValValues))
            #print 'Rows,unsatValValues : '+str(self.unsatVal[0]) 
            self.values = numpy.vstack((self.valueTuple,self.unsatVal))
            valuesTuple = tuple(self.values)
            lines0 = sorted(valuesTuple,key= lambda valuesTuple:float(valuesTuple[0]))
            linesIndex, linesVal = numpy.hsplit(numpy.array(lines0),2)
            
            self.values = [float(linesVal[index][0]) for index in range(len(linesVal))]
            return self.values
        else:
            raise ValueError

            
    

            
            





			
				
class ServiceProcess(object):
	
	def __init__(self):
		#text distribution parameters
		self.textRegionProb = [0.676251331203408,0.082570110046148,0.241178558750444] #put correct values
		#text linear a*x+b region 1
		self.a_text = 0.000062487067042 #put correct values
		self.b_text = 6.216397692662444    #put correct values
		self.mu_text_reg1 = -0.220738 #put correct values
		self.sigma_text_reg1 = 1.22032  #put correct values
		
		#text region 2
		self.mu_text_reg2 = 2.11604 #put correct values
		self.sigma_text_reg2 = 0.058458 #put correct values
		#text region 3
		self.mu_text_reg3 = 4.67307 #put correct values
		self.sigma_text_reg3 = 0.496876 #put correct values
		#image distribution parameters
		self.imageRegionProb= [0.729493365500603,0.256936067551267,0.013570566948130] #put correct values
		
		#image linear a*x+b region 1
		self.a_image = 0.000025935926222 #put correct values
		self.b_image = 3.142696522676892    #put correct values
		self.mu_image_reg1 = 0.00360164 #put correct values
		self.sigma_image_reg1 = 0.0747381  #put correct values
		#image region 2
		self.mu_image_reg2 = 4.05502 #put correct values
		self.sigma_image_reg2 = 0.444086 #put correct values
		#image region 3
		self.mu_image_reg3 = 2.20961 #put correct values
		self.sigma_image_reg3 = 0.0448691 #put correct values
		
		#image region 3
		self.mu_image_reg3 = 2.20961 #put correct values
		self.sigma_image_reg3 = 0.0448691 #put correct values
		
		#script distribution parameters
		#script linear a*x+b region 1
		self.a_script = 0.000078521690109 #put correct values
		self.b_script = 4.798668009026092    #put correct values
		self.mu_script_reg1 = -0.131002 #put correct values
		self.sigma_script_reg1 = 0.883785  #put correct values
		
		#Document distribution parameters
		self.a_documents = 0.3777636241
		self.b_documents = -2.2921606522
		self.c_documents = -0.8518695578
		
		#Err distribution logistic
		self.mu_documents = 0.195262
		self.sigma_documents = 1.49469
		
		self.uncatRegionProb = [0.892245,0.048163,0.05959183] #Uncategorized distribution parameters
		self.c_Uncategorized_reg1 = 0.169453 # Region 1
		self.scale_Uncategorized_reg1 = 0.486268
		self.loc_uncat_reg1 = 3.42806
		
		self.c_Uncategorized_reg2 = 1.0794 # Region 2
		self.scale_Uncategorized_reg2 = 0.62208 # gen extream val
		self.loc_uncat_reg2 = 10.4406
		
		self.c_Uncategorized_reg3 = 1.78841 #Region 3
		self.scale_Uncategorized_reg3 = 0.241476 #gen pareto
		self.loc_uncat_reg3 = 22
		  
		
		###Make it Object oriented ###
		#def __init__(self):
		#   self = self
		#getcontext().prec = 10
	
	def serviceTime(self,category,contSize,globalVar):
		try:
			self.size = long(contSize)
		except:
			self.size = 0
			
			
		
		self.category = category
		self.time = 0.000000
		self.globalVar = globalVar
		if self.size>5*1024*1024:
			self.size=5*1024*1024
		#self.globalVar.rand = random.mtrand.RandomState()
		#Global_var.rand.seed(self.size)
		if string.find(self.category,str('text'))!= -1:
			prob = self.globalVar.rand.uniform()
			
			if prob < self.textRegionProb[0]: #linear region
				timeEst = self.a_text*self.size + self.b_text
				#cdf = Global_var.rand.random()
				timeErr =stats.logistic.rvs(loc=self.mu_text_reg1,scale=math.sqrt(3*self.sigma_text_reg1**2/(constants.pi)**2))
				#timeErr = ServiceProcess.sigma_text_reg1*math.log(cdf/(1.0-cdf)) + ServiceProcess.mu_text_reg1  #inverse cdf of logistic distribution
				self.time = timeEst+timeErr
				self.time = abs(self.time)
			elif self.textRegionProb[0]<= prob < self.textRegionProb[1]+self.textRegionProb[0]: #region 2
				#cdf = Global_var.rand.random()
				self.time = stats.logistic.rvs(loc=self.mu_text_reg2,scale=math.sqrt(3*self.sigma_text_reg2**2/(constants.pi)**2))
				self.time = abs(self.time)
				
			else: #region 3
				#cdf = Global_var.rand.random()
				self.time = stats.logistic.rvs(loc=self.mu_text_reg3,scale=math.sqrt(3*self.sigma_text_reg3**2/(constants.pi)**2))
				self.time = abs(self.time)
			
		elif string.find(self.category,str('image')) != -1:
			prob = self.globalVar.rand.uniform()
			
			if prob < self.imageRegionProb[0]: #linear region
				timeEst = self.a_image*self.size + self.b_image
				timeErr =stats.logistic.rvs(loc=self.mu_image_reg1,scale=math.sqrt(3*self.sigma_image_reg1**2/(constants.pi)**2))
				self.time = timeEst+timeErr
				self.time = abs(self.time)
				
			elif self.imageRegionProb[0]<= prob < self.imageRegionProb[1]+self.imageRegionProb[0]: #region 2
			
				#cdf = float(Global_var.rand.random())
				self.time=stats.logistic.rvs(loc=self.mu_image_reg2,scale=math.sqrt(3* self.sigma_image_reg2**2/(constants.pi)**2))
				#self.time = ServiceProcess.sigma_image_reg2*math.log(cdf/(1-cdf)) + ServiceProcess.mu_image_reg2
				self.time = abs(self.time)
				
			else: #region 3
				#cdf = Global_var.rand.random()
				self.time=stats.logistic.rvs(loc=self.mu_image_reg3,scale=math.sqrt(3* self.sigma_image_reg3**2/(constants.pi)**2))
				#self.time = ServiceProcess.sigma_image_reg3*math.log(cdf/(1-cdf)) + ServiceProcess.mu_image_reg3
				self.time = abs(self.time)
				
		elif string.find(self.category,str('script'))!= -1:
			timeEst = self.a_script*self.size + self.b_script
			#cdf = float(Global_var.rand.random())
			timeErr = stats.logistic.rvs(loc=self.mu_script_reg1,scale=math.sqrt(3*self.sigma_script_reg1**2/(constants.pi)**2))
			#timeErr = ServiceProcess.sigma_script_reg1*math.log(cdf/(1-cdf)) + ServiceProcess.mu_script_reg1  #inverse cdf of logistic distribution
			self.time = float(timeEst+timeErr)
			self.time = abs(self.time)
			
		elif string.find(self.category,str('documents'))!=-1:
			if self.size != 0:
				timeEst = self.a_documents*math.log(self.size)**2+self.b_documents*math.log(self.size)+self.c_documents
			else:
				timeEst = self.c_documents 
			timeErr = stats.logistic.rvs(loc=self.mu_documents,scale=math.sqrt(3*self.sigma_documents**2/(constants.pi)**2))
			self.time = float(timeEst+timeErr)
			self.time = abs(self.time)
			
		else:
			prob = self.globalVar.rand.uniform()
			if prob < self.uncatRegionProb[0]:
				self.time = min(abs(stats.genextreme.rvs(self.c_Uncategorized_reg1,loc = self.loc_uncat_reg1,scale=self.scale_Uncategorized_reg1)),10.0)
			elif self.uncatRegionProb[0]<= prob < self.uncatRegionProb[0] + self.uncatRegionProb[1]:
				self.time = min(max(abs(stats.genextreme.rvs(self.c_Uncategorized_reg2,loc=self.loc_uncat_reg2,scale=self.scale_Uncategorized_reg2)),10.0),22.0)
			else:
				self.time = min(max(abs(stats.genpareto.rvs(self.c_Uncategorized_reg3,loc=self.loc_uncat_reg3,scale=self.scale_Uncategorized_reg3)),22.0),531.46200192986464)

			
		#print float(self.time/1000)
		
		return abs(self.time/1000.0)









class Content(Process):
    
    def __init__(self,size,type,servetime,id,numLines,globalVar):
    	
    	Process.__init__(self,sim=globalVar.process, name = str(id))
        #getcontext().prec = 10
        #self.serviceProObj = ServiceProcess()
        self.type = type
        #self.sim = globalVar.process
        
        self.arrTime = globalVar.process.now()
        self.size = size
        self.id = id
        #self.isQueued = 0
        self.numLines = numLines
        self.serviceTime = servetime
        
         
         
    def run(self,globalVar):
    	
    	self.work = float(globalVar.workload.pop(0))
        globalVar.workload.append(float(self.serviceTime+self.work))
        self.queueLength = globalVar.queueLength.pop(0)
        globalVar.queueLength.append(self.queueLength+self.size)
        globalVar.queueLengthMon.observe(float(globalVar.queueLength[0]))
        #print 'ID:'+str(self.id) + 'workload:'+str(globalVar.workload)
        globalVar.workLoadMon.observe(float(globalVar.workload[0]))
        #print 'Add :'+str(self.serviceTime)
        yield request,self,globalVar.processorCores
        #print 'In Service for:' + str(self.serviceTime)
        yield hold,self,float(self.serviceTime)
        yield release,self,globalVar.processorCores
        if self.id%100000 == 0:
        		print str(self.id) + 'Departed'
        self.work = float(globalVar.workload.pop(0))
        globalVar.workload.append(float(max(self.work-self.serviceTime,0.0)))
        globalVar.workLoadMon.observe(float(globalVar.workload[0]))
        self.queueLength = long(globalVar.queueLength.pop(0))
        globalVar.queueLength.append(long(self.queueLength-long(self.size)))
        globalVar.queueLengthMon.observe(float( globalVar.queueLength[0])) 
        globalVar.waitTimeMon.observe(float(globalVar.process.now()-self.arrTime))         
        
        if self.id >= self.numLines-1:
            print 'Stop'
            globalVar.process.stopSimulation()
            
        del self		








