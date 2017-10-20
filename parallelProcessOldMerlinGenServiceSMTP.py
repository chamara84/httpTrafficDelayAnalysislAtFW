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
import WrokLoadForAllWithoutMainMerlinGenServSMTP
#import matplotlib.pyplot as plt  
#from decimal import *


def simulate(scalePar, meanInterArr,lines,scoresService):
	scaleParSim = scalePar
	#seed = long(seed)
	#file = open('/Users/umdevana/Documents/Python_scripts/ArrivalInfomationAnonNew.csv','rb')
	#lines=numpy.array(list(csv.reader(file)))
	#lines= numpy.hsplit(lines,numpy.array([4,6]))
	#lines = lines[0]
	#getcontext().prec = 10
	arrtime=max(float(lines[0][0]),0.0)
	#print arrtime
	try:
		size = long(lines[0][2])
	except:
		size = 0
	contentType=lines[0][1]
	packetID = 0
	numberOfcores = 1
	globalVar =WrokLoadForAllWithoutMainMerlinGenServSMTP.Global_var()
	print 'In Simulate:'+str(scaleParSim)
	#processorCores = [Resource(numberOfcores,name = ID+str(i)) for i in range(5) ]
	globalVar.workload = 0.0
	globalVar.process.initialize()
	globalVar.workLoadMon.reset()
	globalVar.waitTimeMon.reset()
	globalVar.queueLengthMon.reset()
	globalVar.processorCores.waitMon.reset()
	globalVar.processorCores.actMon.reset()
	arrProcess =WrokLoadForAllWithoutMainMerlinGenServSMTP.Arrival(arrtime,contentType,size,packetID,scaleParSim,globalVar,lines,scoresService)
	globalVar.process.activate(arrProcess,arrProcess.run(globalVar),at=globalVar.process.now() )
	globalVar.process.simulate(until=10000000000)
	probWaitGreat10ms = float(globalVar.numWaitGret10ms)/float(len(lines))
	print str(globalVar.process.now())
	lines = []
	
	#print 'Service Var : ' + str(numpy.var(globalVar.serviceTimesMon))
	
	return [globalVar.workLoadMon.timeAverage(),globalVar.queueLengthMon.timeAverage(),globalVar.waitTimeMon.mean(),(globalVar.processorCores.waitMon.timeAverage()+globalVar.processorCores.actMon.timeAverage()),globalVar.serviceTimesMon.mean(),globalVar.serviceTimesMon.var(),globalVar.interArrivalTime.mean(),scaleParSim,probWaitGreat10ms]
	#return [globalVar.workLoadMon.timeAverage(),(globalVar.processorCores.waitMon.timeAverage()+globalVar.processorCores.actMon.timeAverage()),globalVar.serviceTimesMon.mean(),globalVar.serviceTimesMon.var(),globalVar.interArrivalTime.mean(),scaleParSim]

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
	probWaitGret10Vec = []
	probWaitGret10VarVec = []
	
	[scale,utilization,meanInterArr,lines,scoresService] = getScalePar()
	print 'InterArrivaltime for unscaled : '+str(meanInterArr)
	#print utilization
	scaleParVec = [scale*(index+1) for index in range(9)]
	utilizationVec = [0.1*(index+1) for index in range(9)]
	jobServer = pp.Server(ppservers = (),restart=True)
	meanInterArrVec = []
	#print str(scaleParVec)
	#print str(meanInterArrVec)
	#file = open('/Users/umdevana/Documents/Python_scripts/ArrivalInfomationAnonNew.csv','rb')
	#lines=numpy.array(lines)
	rand = random.mtrand.RandomState()
	
	for scalePar in scaleParVec:
		[scale,utilization,meanInterArr,lines,scoresService] = getScalePar()
		data = list([])
		workLoad =list([])
		queueLength = list([])
		queueSizeInNum = list([])
		waitTime = list([])
		simInstances = list([])
		serviceMean =list([])
		serviceVar =list([])
		arrivalMean =list([])
		linesScaled = list([])
		probWaitGret10 = list([])
		
		# New code
		if scalePar <=1.0:
			for lineNum in range(len(lines)):
				if rand.uniform()<=float(scaleParVec[scaleParIndex]):
					linesScaled.append(lines[lineNum])
				else:
					continue
		else:
			startTime = lines[0][0]
			for line in lines:
				linesScaled.append(line)
			for lineNum in range(len(lines)):
				linesScaled[lineNum][0] = float(lines[lineNum][0])%(((float(lines[-1][0])-float(startTime))/float(scalePar)))
			
				
		
		linesScaled = numpy.array(linesScaled,dtype={'names':('ArrTime','type','size'),'formats':('f8','S10','i8')})			
		linesScaled= numpy.sort(linesScaled,order ='ArrTime' )	
		
		##end new code
		print str(scalePar)
		
		for numleft in range(int(numberOfparallelSims)):
			simInstances.append(jobServer.submit(simulate,(scalePar,meanInterArr,linesScaled,scoresService),(),("SimPy.Simulation","numpy","numpy.random","scipy.stats","scipy.constants","WrokLoadForAllWithoutMainMerlinGenServSMTP","csv","string" )))
			
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
		
		for index in range(int(numberOfparallelSims)):
			probWaitGret10.append(float(data[index][8]))
		
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
		probWaitGret10Vec.append(numpy.mean(probWaitGret10))
		probWaitGret10VarVec.append(numpy.std(probWaitGret10))
		
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/antispamCategorize/src/workloadInfomationMerlinGenServSMTP.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(meanWorkLoadVec)
	w.writerow(stdWorkLoadVec)
	file.close()
	
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/antispamCategorize/src/queueLengthInfomationMerlinGenServSMTP.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(averageQueueLengthVec)
	w.writerow(stdQueueLengthVec)
	file.close()
	
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/antispamCategorize/src/waitInfomationMerlinGenServSMTP.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(averageWaitVec)
	w.writerow(stdWaitVec)
	file.close()
	
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/antispamCategorize/src/queueSizeInNumberMerlinGenServSMTP.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(averageQueuesizeVec)
	w.writerow(stdQueuesizeVec)
	file.close()
	
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/antispamCategorize/src/service_ArrTimeMerlinGenServSMTP.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(serviceMeanVec)
	w.writerow(serviceVarVec)
	w.writerow(meanInterArrVec)
	file.close()
	
	file = open('/Volumes/Home/Python_scripts/NetBeansProjects/antispamCategorize/src/probWaitGret10msMerlinGenServSMTP.txt','wb')
	w = csv.writer(file)
	w.writerow(utilizationVec)
	w.writerow(probWaitGret10Vec)
	w.writerow(probWaitGret10VarVec)
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
	#file = open('/Users/umdevana/Documents/Python_scripts/ArrivalInfomationAnonNew.csv','rb')
	lines=numpy.genfromtxt('/Volumes/Home/Python_scripts/NetBeansProjects/antispamCategorize/src/ArrivalInfomationSMTPTRMerlin.csv',dtype={'names':('ArrTime','type','size'),'formats':('f8','S10','i8')},delimiter=',',missing_values=[0.0,'unknown',0],skip_header = 0)

	print 'Total Sim time : ' + str(float(lines[-1][0])-float(lines[0][0]))
	arrtime=float(lines[0][0])
	scalePar = 1
	#print arrtime
	size = int(lines[0][2])
	contentType=lines[0][1]
	serviceTime = 0.0
	serviceTimeSquare = 0.0
	prevArrTime = 0.0
	InterArrTime = 0.0
	InterArrTimeSquare  = 0.0
	serviceTimeFunc =WrokLoadForAllWithoutMainMerlinGenServSMTP.ServiceProcess() 
	serviceTimeVec = list([])
	scoresService = list([])
	globalVar =WrokLoadForAllWithoutMainMerlinGenServSMTP.Global_var()
	for index in range(len(lines)):
		if index%100000 == 0:
			print str(len(lines)-index)
		#serviceTime = numpy.append(serviceTime,serviceTimeFunc.serviceTime(lines[index][1],lines[index][3],globalVar))
		if index == 0:
			serviceTime = serviceTimeFunc.serviceTime(lines[index][1],lines[index][2],globalVar)
			serviceTimeVec.append(serviceTime)
			serviceTimeSquare = (serviceTimeFunc.serviceTime(lines[index][1],lines[index][2],globalVar))**2
			InterArrTime = 0.0
			InterArrTimeSquare = 0.0
		else:
			InterArrTime = InterArrTime+max(float(lines[index][0])-float(lines[index-1][0]),0.0)
			serviceTimeInstant = serviceTimeFunc.serviceTime(lines[index][1],lines[index][2],globalVar)
			serviceTime = serviceTime + serviceTimeInstant
			serviceTimeSquare = serviceTimeSquare + (serviceTimeInstant)**2
			serviceTimeVec.append(serviceTimeInstant)
			InterArrTimeSquare = InterArrTimeSquare + (max(float(lines[index][0])-float(lines[index-1][0]),0.0))**2
	#print 'Service Time Var'+str(numpy.var(serviceTime))	
	#file = open('/Users/umdevana/Documents/Python_scripts/Inter_ArrTimeTrace.csv','wb')
	#w = csv.writer(file)
	#w.writerow(InterArrTime)
	#file.close()   
	
	utilization = serviceTime/InterArrTime
	
	serviceTimeVec = numpy.array(serviceTimeVec,dtype=float)
	percentileVec = [range(1001)[index]*0.1 for index in range(1001)]
		
	for percentile in  percentileVec:
		scoresService.append(stats.scoreatpercentile(serviceTimeVec,percentile))
			
	scoresService = numpy.array(scoresService,dtype=float)
	serviceTimeVec = []
	
	print 'Mean service Time : '+ str(serviceTime/len(lines))
	print 'Var Service Time:'+str((serviceTimeSquare/len(lines) - (serviceTime/len(lines))**2))
	
	scale = scalePar/utilization*0.1
	meanInterArr = InterArrTime/len(lines)
	varInterArr =  InterArrTimeSquare/len(lines) - (InterArrTime/len(lines))**2
	
	print 'arrival process mean and Var : '+ str([meanInterArr,varInterArr])
	
	return [scale,utilization,meanInterArr,lines,scoresService]
	
if __name__ == "__main__": main()
