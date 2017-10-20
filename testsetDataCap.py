import re
import csv

file = open('/Volumes/Home-2/Users/umdevana/Python_scripts/logs/ts/vid.antivirus.txt','rb')
lines = list(file.readlines())
splitlines = [line.split() for line in lines]
data = []

for splitline in splitlines:
	try:
		mins = int(splitline[-1].split('m')[0])
		sec = float(splitline[-1].split('m')[1].rstrip('s'))
		data.append([long(splitline[1]), float(mins)*60+float(sec)])
	except:
		print splitline

w = csv.writer(open('/Volumes/Home-2/Users/umdevana/Python_scripts/NetBeansProjects/testSetmodel/datavid.csv', 'wb'))

for dataitem in data:
	w.writerow(dataitem)
	

