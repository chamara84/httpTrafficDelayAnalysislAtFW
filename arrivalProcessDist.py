import csv

file = open('/Volumes/Home-1/Users/umdevana/Python_scripts/logs/ArrivalInfomation.txt','rb')
lines = list(csv.reader(file))
numText = 0
interArrTimesText = []
sizeText = []
numScript = 0
interArrTimesScript = []
sizeScript = []
numImage = 0
interArrTimesImage = []
sizeImage = []
numDocuments = 0
interArrTimesDocuments = []
sizeDocuments = []
numOther = 0
interArrTimesOther = []
sizeOther = []

for line in lines:
	if line[1] == 'text':
		numText = numText + 1
		sizeText.append(line[3])
		if len(interArrTimesText) == 0:
			interArrTimesText.append([0.0, long(line[3])])
			prevArrTimeText = float(line[0])
		else:
			interArrTimesText.append([max(0.0,(float(line[0])-prevArrTimeText)), line[3]])
			prevArrTimeText = float(line[0])
			
	elif line[1] == 'image':
		numImage = numImage + 1
		sizeImage.append(line[3])
		if len(interArrTimesImage) == 0:
			interArrTimesImage.append([0.0, line[3]])
			prevArrTimeImage = float(line[0])
		else:
			interArrTimesImage.append([max(0.0,(float(line[0])-prevArrTimeImage)), line[3]])
			prevArrTimeImage = float(line[0])
			
	elif line[1] == 'script':
		numScript = numScript+1
		sizeScript.append(line[3])
		if len(interArrTimesScript) == 0:
			interArrTimesScript.append([0.0, line[3]])
			prevArrTimeScript = float(line[0])
		else:
			interArrTimesScript.append([max(0.0,(float(line[0])-prevArrTimeScript)), line[3]])
			prevArrTimeScript = float(line[0])
			
	elif line[1] == 'documents':
		numDocuments=numDocuments+1
		sizeDocuments.append(line[3])
		if len(interArrTimesDocuments) == 0:
			interArrTimesDocuments.append([0.0, line[3]])
			prevArrTimeDocuments = float(line[0])
		else:
			interArrTimesDocuments.append([max(0.0,(float(line[0])-prevArrTimeDocuments)), line[3]])
			prevArrTimeDocuments = float(line[0])
		
	else:
		numOther = numOther+1
		sizeOther.append(line[3])
		if len(interArrTimesOther) == 0:
			interArrTimesOther.append([0.0, line[3]])
			prevArrTimeOther = float(line[0])
		else:
			interArrTimesOther.append([max(0.0,(float(line[0])-prevArrTimeOther)), line[3]])
			prevArrTimeOther = float(line[0])
		
file = open('/Volumes/Home-1/Users/umdevana/Python_scripts/NetBeansProjects/ArrivalProcessDist/probabilities.csv','wb')
probWrite = csv.writer(file)
probWrite.writerow(['text',float(float(numText)/(float(numText+numScript+numImage+numDocuments+numOther)))])
probWrite.writerow(['script',float(float(numScript)/(float(numText+numScript+numImage+numDocuments+numOther)))])
probWrite.writerow(['image',float(float(numImage)/(float(numText+numScript+numImage+numDocuments+numOther)))])
probWrite.writerow(['documents',float(float(numDocuments)/(float(numText+numScript+numImage+numDocuments+numOther)))])
probWrite.writerow(['other',float(float(numOther)/(float(numText+numScript+numImage+numDocuments+numOther)))])

print 'Text :'+str(numText)
print 'Image :'+str(numImage)
print 'Script :'+str(numScript)
print 'Documents:'+str(numDocuments)
print 'Other:'+str(numOther)  

file.close()

fileText = open('/Volumes/Home-1/Users/umdevana/Python_scripts/NetBeansProjects/ArrivalProcessDist/InterArrSizeText.csv','wb')
write = csv.writer(fileText)
for arrTime in interArrTimesText:
	write.writerow(arrTime)

fileText.close()

fileImage = open('/Volumes/Home-1/Users/umdevana/Python_scripts/NetBeansProjects/ArrivalProcessDist/InterArrSizeImage.csv','wb')
write = csv.writer(fileImage)
for arrTime in interArrTimesImage:
	write.writerow(arrTime)

fileImage.close()

fileScript = open('/Volumes/Home-1/Users/umdevana/Python_scripts/NetBeansProjects/ArrivalProcessDist/InterArrSizeScript.csv','wb')
write = csv.writer(fileScript)
for arrTime in interArrTimesScript:
	write.writerow(arrTime)

fileScript.close()

fileDocuments = open('/Volumes/Home-1/Users/umdevana/Python_scripts/NetBeansProjects/ArrivalProcessDist/InterArrSizeDocuments.csv','wb')
write = csv.writer(fileDocuments)
for arrTime in interArrTimesDocuments:
	write.writerow(arrTime)

fileDocuments.close()

fileOther = open('/Volumes/Home-1/Users/umdevana/Python_scripts/NetBeansProjects/ArrivalProcessDist/InterArrSizeOther.csv','wb')
write = csv.writer(fileOther)
for arrTime in interArrTimesOther:
	write.writerow(arrTime)

fileOther.close()








