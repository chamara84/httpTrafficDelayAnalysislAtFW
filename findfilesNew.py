import csv
import os
import numpy
import random
import time

class GetFileNames(object):
    def __init__(self,path):
        self.path = path
        self.listFiles = list([])
        self.holidays = set([('May','21')])
        self.weekDays = set(['Mon','Tue','Wed','Thu','Fri'])
    
    def findFiles(self,timePeriod):
        filenames = os.listdir(self.path) 
        
        for fileName in filenames:
            startTimeUnix = time.ctime(float(fileName.split('_')[1]))
            dayofWeek =startTimeUnix.split()[0]
            timeOfDay = startTimeUnix.split()[3]
            hour = int(timeOfDay.split(':')[0])
            dayOfMonth = (startTimeUnix.split()[1],startTimeUnix.split()[2])
            
            if hour == int(timePeriod[0]) and dayofWeek in self.weekDays and dayOfMonth not in self.holidays:
                self.listFiles.append(fileName)
            
            else:
                continue
        #print str(self.listFiles)
        return self.listFiles
        

#getFile = GetFileNames('/Users/umdevana/Documents/Python_scripts/hourly/')
#listFiles = getFile.findFiles([9,10])
#print str(listFiles)

class StitchFiles(object):
	def __init__(self,listFiles):
		self.listFiles = listFiles
		self.files = []
		self.setOfFiles =[]
		self.setOfFileSets = []
		
	def findFilesCloseIntime(self):
		
		for index in range(len(self.listFiles)):
			startTimeOfFile = float(self.listFiles[index].split('_')[1])
			self.files.append([startTimeOfFile,self.listFiles[index] ])
		
		self.files = dict(self.files)
		keysOfFiles = self.files.keys()
		keysOfFiles = sorted(keysOfFiles)
		
		for key in keysOfFiles:
			for index in range(len(keysOfFiles)):
				if  abs(float(keysOfFiles[index])-float(key)) <= 3600.0 and keysOfFiles[index] in self.files :
					self.setOfFiles.append(self.files.pop(keysOfFiles[index]))
					
				else:
					continue
			if len(self.setOfFiles)>0 :
				self.setOfFileSets.append(self.setOfFiles)
				
			self.setOfFiles = []
			
		return self.setOfFileSets
			
	def getLinesInFileSet(self,setOfFiles,folder):
		
		for index in range(len(setOfFiles)):
			
			if index == 0:
				lines=numpy.genfromtxt(str(folder)+str(setOfFiles[index]),dtype={'names':('ArrTime','type','size'),'formats':('f8','S10','i8')},delimiter=',',missing_values=[0.0,'unknown',0],skip_header = 1)
				lines= numpy.sort(lines,order = 'ArrTime')
				lines = list(lines)
				
				startTime = max(lines[0][0],0.0)
				for indexLines in range(len(lines)):
					lines[indexLines][0] = max(lines[indexLines][0]-startTime,0.0)
				
			else: 
				firstTimeStampPrev = float(setOfFiles[index-1].split('_')[1])
				timeHuman = time.ctime(firstTimeStampPrev)
				DatePrev = (timeHuman.split()[1],timeHuman.split()[2])
				firstTimeStampCur = float(setOfFiles[index].split('_')[1])
				timeHuman = time.ctime(firstTimeStampCur)
				DateCur = (timeHuman.split()[1],timeHuman.split()[2])
				if DateCur == DatePrev:
					lastTimeStamp = line[-1]['ArrTime']
					tempLines =numpy.genfromtxt(str(folder)+str(setOfFiles[index]),dtype={'names':('ArrTime','type','size'),'formats':('f8','S10','i8')},delimiter=',',missing_values=[0.0,'unknown',0],skip_header = 1)
					tempLines= numpy.sort(tempLines,order = 'ArrTime')
					tempLines = list(tempLines)
				
                                	startTime = max(tempLines[0][0],0.0)
                                	for indexLines in range(len(tempLines)):
                                        	tempLines[indexLines][0] = max(tempLines[indexLines][0]-startTime,0.0)+lastTimeStamp
						lines.append(tempLines[indexLines])
				else:
					tempLines =numpy.genfromtxt(str(folder)+str(setOfFiles[index]),dtype={'names':('ArrTime','type','size'),'formats':('f8','S10','i8')},delimiter=',',missing_values=[0.0,'unknown',0],skip_header = 1)
					tempLines= numpy.sort(tempLines,order = 'ArrTime')
					tempLines = list(tempLines)
				
                                	startTime = max(tempLines[0][0],0.0)
                                	for indexLines in range(len(tempLines)):
                                        	tempLines[indexLines][0] = max(tempLines[indexLines][0]-startTime,0.0)
						lines.append(tempLines[indexLines])
					
				 
		
					
		lines = numpy.array(lines,dtype={'names':('ArrTime','type','size'),'formats':('f8','S10','i8')})
		lines = numpy.sort(lines,order = 'ArrTime')		
		#lines= sorted(lines,key= lambda lines: float(lines[0]))
		lines = numpy.array(lines,dtype={'names':('ArrTime','type','size'),'formats':('f8','S10','i8')})		
		return lines
		
		
#getFile = GetFileNames('/Users/umdevana/Documents/Python_scripts/hourly/')
#listFiles = getFile.findFiles([9,10])
#print str(listFiles)

#group =StitchFiles(listFiles)


#setOfSetOfFiles = group.findFilesCloseIntime()
#print str(setOfSetOfFiles)
#numpy.random.shuffle(setOfSetOfFiles)
#print str(setOfSetOfFiles)
#print 'length',len(setOfSetOfFiles)
#lines = group.getLinesInFileSet(setOfSetOfFiles[0],'/Users/umdevana/Documents/Python_scripts/hourly/') 
#file = open('/Users/umdevana/Documents/hourly.csv','wb')
#w = csv.writer(file)	

#for line in lines:
#	w.writerow(line)
	
		
			
		
			
					
						
			
			


                

            

    
