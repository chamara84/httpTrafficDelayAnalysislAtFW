from scipy import stats
from scipy import constants
import csv
from decimal import *
from numpy import random
import math

class ServiceProcess():

    #text distribution parameters
    textRegionProb = [0.676251331203408,0.082570110046148,0.241178558750444] #put correct values
    #text linear a*x+b region 1
    a_text = 0.000062487067042 #put correct values
    b_text = 6.216397692662444    #put correct values
    mu_text_reg1 = -0.220738 #put correct values
    sigma_text_reg1 = 1.22032  #put correct values

    #text region 2
    mu_text_reg2 = 2.11604 #put correct values
    sigma_text_reg2 = 0.058458 #put correct values

    #text region 3
    mu_text_reg3 = 4.67307 #put correct values
    sigma_text_reg3 = 0.496876 #put correct values

#image distribution parameters
    imageRegionProb= [0.729493365500603,0.256936067551267,0.013570566948130] #put correct values

    #image linear a*x+b region 1

    a_image = 0.000025935926222 #put correct values
    b_image = 3.142696522676892    #put correct values
    mu_image_reg1 = 0.00360164 #put correct values
    sigma_image_reg1 = 0.0747381  #put correct values

    #image region 2
    mu_image_reg2 = 4.05502 #put correct values
    sigma_image_reg2 = 0.444086 #put correct values

    #image region 3
    mu_image_reg3 = 2.20961 #put correct values
    sigma_image_reg3 = 0.0448691 #put correct values

#script distribution parameters
	#script linear a*x+b region 1

    a_script = 0.000078521690109 #put correct values
    b_script = 4.798668009026092    #put correct values
    mu_script_reg1 = -0.131002 #put correct values
    sigma_script_reg1 = 0.883785  #put correct values

#Document distribution parameters
    a_documents = 0.3777636241
    b_documents = -2.2921606522
    c_documents = -0.8518695578
    #Err distribution logistic
    mu_documents = 0.195262
    sigma_documents = 1.49469
    
    uncatRegionProb = [0.892245,0.048163,0.05959183] #Uncategorized distribution parameters
    c_Uncategorized_reg1 = 0.169453 # Region 1
    scale_Uncategorized_reg1 = 0.486268
    loc_uncat_reg1 = 3.42806
	  
    
	
    c_Uncategorized_reg2 = 1.0794 # Region 2
    scale_Uncategorized_reg2 = 0.62208 # gen extream val
    loc_uncat_reg2 = 10.4406
    
       
    c_Uncategorized_reg3 = 1.78841 #Region 3
    scale_Uncategorized_reg3 = 0.241476 #gen pareto
    loc_uncat_reg3 = 22
    
    
    

###Make it Object oriented ###
    #def __init__(self):
     #   self = self
    rand = random.mtrand.RandomState(120586)
    def serviceTime(self,category,contSize):
        self.size = long(contSize)
        self.category = category
        self.time = 0.000000
        
        if self.size>5*1024*1024:
            self.size=5*1024*1024

        


        if self.category=='text':
            prob = ServiceProcess.rand.uniform()

            if prob < ServiceProcess.textRegionProb[0]: #linear region
                timeEst = ServiceProcess.a_text*self.size + ServiceProcess.b_text
                #cdf = Global_var.rand.random()
                timeErr =stats.logistic.rvs(loc=ServiceProcess.mu_text_reg1,scale=math.sqrt(3*ServiceProcess.sigma_text_reg1**2/(float(constants.pi))**2))
                #timeErr = ServiceProcess.sigma_text_reg1*math.log(cdf/(1.0-cdf)) + ServiceProcess.mu_text_reg1  #inverse cdf of logistic distribution
                self.time = timeEst+timeErr
                self.time = abs(self.time)
            
            elif ServiceProcess.textRegionProb[0]<= prob and prob< ServiceProcess.textRegionProb[1]+ServiceProcess.textRegionProb[0]: #region 2
                #cdf = Global_var.rand.random()
                self.time = stats.logistic.rvs(loc=ServiceProcess.mu_text_reg2,scale=math.sqrt(3*ServiceProcess.sigma_text_reg2**2/(float(constants.pi))**2))
                self.time = abs(self.time)

            else: #region 3
                #cdf = Global_var.rand.random()
                self.time = stats.logistic.rvs(loc=ServiceProcess.mu_text_reg3,scale=math.sqrt(3*ServiceProcess.sigma_text_reg3**2/(float(constants.pi))**2))
                self.time = abs(self.time)

        elif category=='images':
        	prob = ServiceProcess.rand.uniform()
        	
        	if prob < ServiceProcess.imageRegionProb[0]:
        		#linear region
        		timeEst = ServiceProcess.a_image*self.size + ServiceProcess.b_image
        		timeErr =stats.logistic.rvs(loc=ServiceProcess.mu_image_reg1,scale=math.sqrt(3*ServiceProcess.sigma_image_reg1**2/(constants.pi)**2))
        		self.time = timeEst+timeErr
        		self.time = abs(self.time)
        		
        	elif ServiceProcess.imageRegionProb[0]<= prob and  prob< ServiceProcess.imageRegionProb[1]+ServiceProcess.imageRegionProb[0]:
        	   	self.time=stats.logistic.rvs(loc=ServiceProcess.mu_image_reg2,scale=math.sqrt(3* ServiceProcess.sigma_image_reg2**2/(constants.pi)**2)) #region 2
        	   	self.time = abs(self.time)
        	   	
        	else: #region 3
        		self.time=stats.logistic.rvs(loc=ServiceProcess.mu_image_reg3,scale=math.sqrt(3* ServiceProcess.sigma_image_reg3**2/(constants.pi)**2))
        		self.time = abs(self.time)
        		
        	

        elif category=='script':
            timeEst = ServiceProcess.a_script*self.size + ServiceProcess.b_script
            #cdf = float(Global_var.rand.random())
            timeErr = stats.logistic.rvs(loc=ServiceProcess.mu_script_reg1,scale=math.sqrt(3*ServiceProcess.sigma_script_reg1**2/(constants.pi)**2))
            #timeErr = ServiceProcess.sigma_script_reg1*math.log(cdf/(1-cdf)) + ServiceProcess.mu_script_reg1  #inverse cdf of logistic distribution
            self.time = float(timeEst+timeErr)
            self.time = abs(self.time)

        elif category == 'documents':
            timeEst = ServiceProcess.a_documents*math.log(self.size)**2+ServiceProcess.b_documents*math.log(self.size)+ServiceProcess.c_documents
            timeErr = stats.logistic.rvs(loc=ServiceProcess.mu_documents,scale=math.sqrt(3*ServiceProcess.sigma_documents**2/(constants.pi)**2))
            self.time = float(timeEst+timeErr)
            self.time = abs(self.time)

        else:
        	prob = ServiceProcess.rand.uniform()
        	if prob < ServiceProcess.uncatRegionProb[0]:
        		self.time = abs(stats.genextreme.rvs(ServiceProcess.c_Uncategorized_reg1,ServiceProcess.loc_uncat_reg1,ServiceProcess.scale_Uncategorized_reg1))
        	elif ServiceProcess.uncatRegionProb[0]<= prob < ServiceProcess.uncatRegionProb[0] + ServiceProcess.uncatRegionProb[1]:
        		self.time = abs(stats.genextreme.rvs(ServiceProcess.c_Uncategorized_reg2,ServiceProcess.loc_uncat_reg2,ServiceProcess.scale_Uncategorized_reg2))
        	else:
        		self.time = abs(stats.genpareto.rvs(ServiceProcess.c_Uncategorized_reg3,ServiceProcess.loc_uncat_reg3,ServiceProcess.scale_Uncategorized_reg3))



        #print float(self.time/1000)


        return abs(self.time/1000.0)        

def main():
	service = ServiceProcess()
	contentType = 'other'
	fileNameAnim = '/Volumes/Home-1/Users/umdevana/Python_scripts/outanimation.csv'
	dataCompressed = '/Volumes/Home-1/Users/umdevana/Python_scripts/outcompressed.csv'
	dataExecutable = '/Volumes/Home-1/Users/umdevana/Python_scripts/outexecutable.csv'
	dataTestSet = '/Volumes/Home-1/Users/umdevana/Python_scripts/NetBeansProjects/testSetmodel/datatestSet.csv'
	dataVid = '/Volumes/Home-1/Users/umdevana/Python_scripts/NetBeansProjects/testSetmodel/datavid.csv'
	dataVideo = '/Volumes/Home-1/Users/umdevana/Python_scripts/outvideo.csv'
	lines=list(csv.reader(open(fileNameAnim,'rb')))
	linesComp = list(csv.reader(open(dataCompressed,'rb')))
	for index in range(len(linesComp)):
		lines.append(linesComp[index])
	linesExec = list(csv.reader(open(dataExecutable,'rb')))
	for index in range(len(linesExec)):
		lines.append(linesExec[index])
	linesDataSet= list(csv.reader(open(dataTestSet,'rb')))
	for index in range(len(linesDataSet)):
		lines.append(linesDataSet[index])
	linesVid = list(csv.reader(open(dataVid,'rb')))
	for index in range(len(linesVid)):
		lines.append(linesVid[index])
	linesVideo = list(csv.reader(open(dataVideo,'rb')))
	for index in range(len(linesVideo)):
		lines.append(linesVideo[index])
	
	#print lines
	genServiceTimes = []
	actualServiceTime = []

	for line in lines:
		genServiceTimes.append(service.serviceTime(contentType,long(line[0])))
		if genServiceTimes[-1] > 1:
			print str(genServiceTimes[-1])
		actualServiceTime.append(float(line[1])/1000.0)

	[D,p]= stats.mstats.ks_twosamp(genServiceTimes,actualServiceTime,alternative='two_sided')

	print 'D : '+str(D)
	print 'p : '+str(p)

	fileTime = open('/Volumes/Home-1/Users/umdevana/Python_scripts/NetBeansProjects/ServiceProcessKSTest/serviceTime'+contentType+'.csv','wb')
	w_time = csv.writer(fileTime)
	
	
	w_time.writerow(genServiceTimes)
	w_time.writerow(actualServiceTime)
		
	fileTime .close()
	
	
if __name__ == "__main__": main()

	
