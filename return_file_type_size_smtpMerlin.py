import re
import string
import numpy

__author__="Chamara"
__date__ ="$Mar 30, 2012 2:21:55 PM$"


import csv





def main():
    fileNames = ['/Volumes/Home/Python_scripts/logs/anon/0_smtp_summary_anon.csv','/Volumes/Home/Python_scripts/logs/anon/1_smtp_summary_anon.csv']
    
    accuracy = 4
    fileVec = [open(fileNames[index],'rb') for index in range(len(fileNames))]

    fsize_names = ['text_fsize','image_fsize','video_fsize','executable_fsize',\
                    'script_fsize','documents_fsize','animation_fsize','compressed_fsize',\
                    'unknown_fsize']
    namesOfTypes = ['text','image','video','executable','script',\
                    'documents','animation','compressed','unknown']

    #text parameters
    textExt = ['jhtml','htm','tex','txt','html','css','rss','orig','shtml',
                'xml','rdf','wml','wtf','pkix-crl','ocsp-response','plain','rss+xml','cross-domain-policy']

    #image parameters
    imageExt = ['jpg','ico','gif','ps','gallery','png','PNG','jpeg','JPG','icon','bmp']

    #video parameters
    videoExt = ['ogg','flv','amf','mp4','fcs']

    #executable parameters
    executableExt = ['do','exe','action','octet-stream']

    #script parameters
    scriptExt = ['cfm','py','json','cgi','phtml','asp','js','jsp','php',\
                'ashx','axd','gne','aspx','dll','jspx','javascript']

    #unknown parameters
    unknownExt = set([])

    #document parameters
    documentsExt = ['g','pdf','msword',]


    #animation parameters
    animationExt = ['swf','shockwave-flash']


    #compressed parameters
    compressedExt = ['rar','zip','gzip','bzip2']

    #arrival information Time, content type, encoding type, size
    arrivalInfo = []


    types = [textExt,imageExt,videoExt,executableExt,scriptExt,\
            documentsExt,animationExt,compressedExt,unknownExt]

    lines0=list(csv.reader(fileVec[0]))
    lines1 = list(csv.reader(fileVec[1]))
    lengthOfData = len(lines0[0])
    contenType_column=lines0[0].index('content-type')
    #encodingType_column=lines0[0].index('content-encoding')
    length_column=lines0[0].index('content-length')
    arrivalTime_column =lines0[0].index('timestamp')
    hashColumn = lines0[0].index('content_hash')
    exitStatus = lines0[0].index('exit_status')
    
    
    lines0 = lines0[1:]
    lines1 = lines1[1:]
    lines0= list(sorted(tuple(lines0),key= lambda lines0: float(lines0[0])))
    lines1= list(sorted(tuple(lines1),key= lambda lines1: float(lines1[0])))
    startTime = min(float(lines0[0][arrivalTime_column]),float(lines1[0][arrivalTime_column]))
    index1 = 0
    index0 = 0
    lenIndex0 = len(lines0)
    lenIndex1 = len(lines1)
    linesTot = []
    
    for index in range(lenIndex0+lenIndex1):
        if (index)%100000 == 0:
            print 'more lines' + str(lenIndex0+lenIndex1 - index)
        
        if index1<lenIndex1 and index0<lenIndex0 and float(lines0[index0][0])<=float(lines1[index1][0]):
                linesTot.append(lines0[index0])
                index0 = index0 +1

        elif index1<lenIndex1 and index0<lenIndex0 and float(lines0[index0][0]) > float(lines1[index1][0]):
                linesTot.append(lines1[index1])
                index1 = index1 +1
        elif index1>=lenIndex1 and index0<lenIndex0:
                linesTot.append(lines0[index0])
                index0 = index0 +1
        elif index0>=lenIndex0 and index1<lenIndex1:
                linesTot.append(lines1[index1])
                index1 = index1 +1
        else:
                print 'wrong'

    print str(len(linesTot))
    		 
    
    lines0 = []
    lines1 = []
    
    for index in range(len(linesTot)):
        if index+1 < len(linesTot) and float(linesTot[index+1][0])<float(linesTot[index][0]) :
            print 'Error in LinesTot'	
    
    unknownContent = []
    
   
    
       

    print 'In processing'
    for line in linesTot:
    	
    	try:
    		status = line[exitStatus]
    	except:
    		continue
    	if string.find(status,str('complete')) != -1:
    		
    		try:
    			contentLength = line[length_column]
    		except:
    			print str(line)
    			contentLength = 0
        	arrivalTime = round(float(max(float(line[arrivalTime_column])-float(startTime),0.0)),accuracy)
        	try:
        		contentStr=line[contenType_column].split('/')[-1]
        	except:
        		contentStr = 'unknown'
        		
        	if re.match(r'^x-', contentStr):
        		contentStr = contentStr.lstrip('x-')
        	try:
        		contentStr = contentStr.split(';')[0]
        	except:
        		try:
        			contentStr = contentStr.split()[0]
        		except:
        			contentStr = contentStr
        			
        	for index_fsize_names in range(len(fsize_names)):
        		if contentStr in types[index_fsize_names]:
        			contentType = namesOfTypes[index_fsize_names]
        			break
        			
        				
        		elif index_fsize_names == 8:
        			contentType = namesOfTypes[index_fsize_names]
        			try:
        				unknownContent.append(line[contenType_column])
        			except:
        				unknownContent.append('Empty')
        				
        			
        	
        	try:
        		hash = line[hashColumn]
        	except:
        		hash = ''
        	       
        	arrivalInfo.append([arrivalTime,contentType,contentLength,hash])
        	
        else:
        	continue
    
    print 'In file writing'
    file = open('/Volumes/Home/Python_scripts/NetBeansProjects/antispamCategorize/src/ArrivalInfomationSMTPTRMerlin.csv','wb')
    w = csv.writer(file)
    for info in arrivalInfo:
        w.writerow(info)
       

    file.close()
    
    file = open('/Volumes/Home/Python_scripts/NetBeansProjects/antispamCategorize/src/SMTPTRUnknownMerlin.txt','wb')
    for info in unknownContent:
        file.write(info)
        file.write('\n')
		
    file.close()
    
    








if __name__ == "__main__":
    main()