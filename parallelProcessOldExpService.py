from SimPy.Simulation import *
#from SimPy.SimPlot import *
#import Queue
import csv
import math
import numpy
from numpy import random
from scipy import stats
from scipy import constants
import pp
import WrokLoadForAllWithoutMainExpService
#import matplotlib.pyplot as plt  
#from decimal import *


def simulate(scalePar, meanInterArr,lines,meanService):
	scaleParSim = scalePar
	meanServiceSim =meanService
	#seed = long(seed)
	
	#getcontext().prec = 10
	arrtime=max(float(lines[0][0]),0.0)
	#print arrtime
	try:
		size = long(lines[0][3])
	except:
		size = 0
	contentType=lines[0][1]
	packetID = 0
	numberOfcores = 1
	globalVar = WrokLoadForAllWithoutMainExpService.Global_var()
	print 'In Simulate:'+str(scaleParSim)
	#processorCores = [Resource(numberOfcores,name = ID+str(i)) for i in range(5) ]
	globalVar.workload = list([0.0])
	globalVar.process.initialize()
	globalVar.workLoadMon.reset()
	globalVar.waitTimeMon.reset()
	globalVar.queueLengthMon.reset()
	globalVar.processorCores.waitMon.reset()
	globalVar.processorCores.actMon.reset()
	arrProcess = WrokLoadForAllWithoutMainExpService.Arrival(arrtime,contentType,size,packetID,scaleParSim,globalVar,lines)
	lines= []
	globalVar.process.activate(arrProcess,arrProcess.run(globalVar,meanService),at=globalVar.process.now() )
	globalVar.process.simulate(until=10000000000)
	print str(globalVar.process.now())
	
	#print 'Service Var : ' + str(numpy.var(globalVar.serviceTimesMon))
	
	return [globalVar.workLoadMon.timeAverage(),globalVar.queueLengthMon.timeAverage(),globalVar.waitTimeMon.mean(),(globalVar.processorCores.waitMon.timeAverage()+globalVar.processorCores.actMon.timeAverage()),numpy.mean(globalVar.serviceTimesMon),numpy.var(globalVar.serviceTimesMon),globalVar.interArrivalTime.mean(),scaleParSim]
	

def main():
	numberOfparallelSims = 10.0
	meanWorkLoadVec = []
	stdWorkLoadVec = []
	averageQueueLengthVec = []
	stdQueueLengthVec = []
	averageWaitVec = []
	stdWaitVec = []
	stdQueuesizeVec =[]
	averageQueuesizeVec =[]
	serviceMeanVec =[]
	serviceVarVec =[]
	[scalePar,utilization,meanInterArr,meanService] = getScalePar()
	print 'InterArrivaltime for unscaled : '+str(meanInterArr)
	#print utilization
	scaleParVec = [scalePar*(index+1) for index in range(9)]
	utilizationVec = [0.1*(index+1) for index in range(9)]
	jobServer = pp.Server(ppservers = ())
	meanInterArrVec = []
	#print str(scaleParVec)
	#print str(meanInterArrVec)
	
	
	for scalePar in scaleParVec:
		file = open('/Volumes/Home/Python_scripts/logs/ArrivalInfomation.txt','rb')
		lines=numpy.array(list(csv.reader(file)))
		data = list([])
		workLoad =list([])
		queueLength = list([])
		queueSizeInNum = list([])
		waitTime = list([])
		simInstances = list([])
		serviceMean =list([])
		serviceVar =list([])
		arrivalMean =list([])
		
		for lineNum in range(len(lines)):
			lines[lineNum][0] = float(lines[lineNum][0])%(((float(lines[-1][0])-float(lines[0][0]))/float(scalePar)))
			
		lines= sorted(lines,key= lambda lines: float(lines[0]))
		
		for index in range(len(lines)-1):
			if float(lines[index][0])> float(lines[index+1][0]):
				print 'Error in lines'
				
		print str(scalePar)
		
		for numleft in range(int(numberOfparallelSims)):
			simInstances.append(jobServer.submit(simulate,(scalePar,meanInterArr,lines,meanService),(),("SimPy.Simulation","numpy","numpy.random","scipy.stats","scipy.constants","WrokLoadForAllWithoutMainExpService","csv","string" )))
			
		for sim in simInstances:
			data.append(sim())
			
		for index in range(int(numberOfparallelSims)):
			workLoad.append(float(data[index][0]))
			
		for index in range(int(numberOfparallelSims)):
			queueLength.append(float(data[index][1]))
			
		for index in range(int(numberOfparallelSims)):
			waitTime.append(float(data[index][2]))
			
		for index in range(int(numberOfparallelSims)):
			queueSizeInNum.append(float(data[index][3]))
		
		for index in range(int(numberOfparallelSims)):
			serviceMean.append(float(data[index][4]))
			
		for index in range(int(numberOfparallelSims)):
			serviceVar.append(float(data[index][5]))
			
		for index in range(int(numberOfparallelSims)):
			arrivalMean.append(float(data[index][6]))
		#print 'ServiceVar : ' + str(serviceVar)
		
		meanWorkLoadVec.append(numpy.mean(workLoad))
		stdWorkLoadVec.append(numpy.std(workLoad))
		averageQueueLengthVec.append(numpy.mean(queueLength))
		stdQueueLengthVec.append(numpy.std(queueLength))
		averageQueuesizeVec.append(numpy.mean(queueSizeInNum))
		stdQueuesizeVec.append(numpy.std(queueSizeInNum))
		averageWaitVec.append(numpy.mean(waitTime))
		stdWaitVec.append(numpy.std(waitTime))
		serviceMeanVec.append(numpy.mean(serviceMean))
		serviceVarVec.append(numpy.mean(serviceVar))
		meanInterArrVec.append(numpy.mean(arrivalMean))
		
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/WrokLoadForContentType/src/workloadInfomationTRTraceExpService.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(meanWorkLoadVec)
	w.writerow(stdWorkLoadVec)
	file.close()
	
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/WrokLoadForContentType/src/queueLengthInfomationTRTraceExpService.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(averageQueueLengthVec)
	w.writerow(stdQueueLengthVec)
	file.close()
	
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/WrokLoadForContentType/src/waitInfomationTRTraceExpService.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(averageWaitVec)
	w.writerow(stdWaitVec)
	file.close()
	
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/WrokLoadForContentType/src/queueSizeInNumberTRTraceExpService.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(averageQueuesizeVec)
	w.writerow(stdQueuesizeVec)
	file.close()
	
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/WrokLoadForContentType/src/service_ArrTimeTRTraceExpService.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(serviceMeanVec)
	w.writerow(serviceVarVec)
	w.writerow(meanInterArrVec)
	file.close()
	
	
	
    
		
	#print 'Workload Time Average:'+str(workLoadVec)
	#print 'Average Queue length in bytes: '+str(averageQueueLengthVec)
	#print 'Average wait time in sec: '+str(averageWaitVec)
	#print 'Scale Parameter : ' + str(scaleParVec)
	
	#plt.figure()
	#plt.errorbar(utilizationVec, meanWorkLoadVec, yerr=stdWorkLoadVec)
	#plt.title("Workload Time Average")
	#plt.xlabel("Utilization")
	#plt.ylabel("Workload (backlog)(sec)")
	#plt.show()
	
	#plt.figure()
	#plt.errorbar(utilizationVec, averageQueueLengthVec, yerr=stdQueueLengthVec)
	#plt.title("Queue length")
	#plt.xlabel("Utilization")
	#plt.ylabel("Queue length (bytes)")
	#plt.show()
	
	#plt.figure()
	#plt.errorbar(utilizationVec, averageWaitVec, yerr=stdWaitVec)
	#plt.title("Average Waiting time")
	#plt.xlabel("Utilization")
	#plt.ylabel("Waiting time (sec)")
	#plt.show()
	
	
    
	
	
	
	
	
def getScalePar():
	file = open('/Volumes/Home/Python_scripts/logs/ArrivalInfomation.txt','rb')
	lines=numpy.array(list(csv.reader(file)))
	print 'Total Sim time : ' + str(float(lines[-1][0])-float(lines[0][0]))
	arrtime=float(lines[0][0])
	scalePar = 1
	#print arrtime
	size = int(lines[0][3])
	contentType=lines[0][1]
	serviceTime = []
	prevArrTime = 0.0
	InterArrTime = []
	serviceTimeFunc =WrokLoadForAllWithoutMainExpService.ServiceProcess() 
	globalVar = WrokLoadForAllWithoutMainExpService.Global_var()
	for index in range(len(lines)):
		serviceTime.append(serviceTimeFunc.serviceTime(lines[index][1],lines[index][3],globalVar))
		if index == 0:
			InterArrTime.append(0.0)	
		else:
			InterArrTime.append(float(lines[index][0])-float(lines[index-1][0]))
			
	#print 'Service Time Var'+str(numpy.var(serviceTime))	
	file = open('/Users/umdevana/Documents/Python_scripts/Inter_ArrTimeTrace.csv','wb')
	w = csv.writer(file)
	w.writerow(InterArrTime)
	file.close()   
	
	utilization = sum(serviceTime)/(float(lines[-1][0])-float(lines[0][0]))
	
	meanService = numpy.mean(serviceTime)
	print 'Mean service Time : '+ str(numpy.mean(serviceTime))
	print 'Var Service Time:'+str(numpy.var(serviceTime))
	
	scale = scalePar/utilization*0.1
	meanInterArr = numpy.mean(InterArrTime)
	varInterArr =  numpy.var(InterArrTime)
	print 'arrival process mean and Var : '+ str([meanInterArr,varInterArr])
	
	return [scale,utilization,meanInterArr,meanService]
if __name__ == "__main__": main()
