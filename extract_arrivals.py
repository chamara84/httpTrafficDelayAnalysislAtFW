import csv
import os
import numpy
import random

class robust_csv_reader(object):

    def __init__(self,filename):
        self.reader=csv.reader(open(filename))

    def next(self):
        success=False
        while True:
            try:
                return self.reader.next()
            except StopIteration:
                return []
            except:
                pass
            






class file_classifier(object):

    def __init__(self):
        Ext={}
        #text parameters
        Ext['text'] = ['jhtml','htm','tex','txt','html','css','rss','orig','shtml',\
                    'xml','rdf','wml','wtf','pkix-crl','ocsp-response','plain','rss+xml','cross-domain-policy']

        #image parameters
        Ext['image'] = ['jpg','ico','gif','ps','gallery','png','PNG','jpeg','JPG','icon','bmp']

        #video parameters
        Ext['video'] = ['ogg','flv','amf','mp4','fcs']

        #executable parameters
        Ext['executable'] = ['do','exe','action','octet-stream']

        #script parameters
        Ext['script'] = ['cfm','py','json','cgi','phtml','asp','js','jsp','php',\
                    'ashx','axd','gne','aspx','dll','jspx','javascript']

        #unknown parameters
        Ext['unknown'] = set([])

        #document parameters
        Ext['documents'] = ['g','pdf','msword',]


        #animation parameters
        Ext['animation'] = ['swf','shockwave-flash']


        #compressed parameters
        Ext['compressed'] = ['rar','zip','gzip','bzip2']

        self.classdict={}
        for ftype in Ext:
            print ftype
            for code in Ext[ftype]:
                self.classdict[code]=ftype
        


    def classify(self,mystring):
        #if string has one of these types in it 
        special=['image','video','script']
        contentStr=mystring.split('/')[0]
        for s in special:
            if s in contentStr:
                return s
            
        #otherwise look after the '/' if there is one
        contentStr=mystring.split('/')[-1].split('x-')[-1].split(';')[0].split(';')[0]
        if contentStr in self.classdict:
            return self.classdict[contentStr]
        else:
            return 'unknown'

def fuzz_time(timestamp):
    num_digits=len(timestamp.split('.')[-1])
    return float(timestamp)+.1**num_digits*random.random()
    



       



timestamps=list(['./smtp_summary_anon.csv'])
file_list={}


fields=['timestamp','content-type','content-length','content_hash','exit_status']


classifier=file_classifier() 
num_done=0
for t in range(len(timestamps)):
    files=timestamps[t]
    print num_done,files
    fp=open(str(t)+'_arrivals_smtp.csv','w')
    w=csv.writer(fp)
    w.writerow(['timestamp','content-type','content-length','content-hash'])
        
    if len(files)>1:
        data={}
        reader=dict([(f,robust_csv_reader(f)) for f in files])
        header2column={}
        max_columns={}
        for f in files:
            headers=reader[f].next()
            header2column[f]=dict([(headers[i],i) for i in range(len(headers))])
            max_columns[f]=max(header2column[f].values())
            line=reader[f].next()
            data[f]=[fuzz_time(line[header2column[f]['timestamp']]),classifier.classify(line[header2column[f]['content-type']])]+\
                     [line[header2column[f][field]] for field in fields[2:]]
        
        num_output=0
        while len(files)>0:
            num_output+=1
            if num_output % 100000 ==0:
                print num_output
            nxt=numpy.argmin([d[0] for d in data.values()])
            f=data.keys()[nxt]
            row=data[f]
            row[0]=str(int(row[0]))+'.'+str(int(1000000*(row[0]-int(row[0]))))
            if data[f][-1]=='complete':
                w.writerow(data[f][:-1])
            
            success=False
            while not success:
                line=reader[f].next()
                if len(line)>max_columns[f]:
                    try:
                        data[f]=[fuzz_time(line[header2column[f]['timestamp']]),classifier.classify(line[header2column[f]['content-type']])]+\
                             [line[header2column[f][field]] for field in fields[2:]]
                        success=True
                    except:
                        pass
                elif len(line)==0:
                    files=[g for g in files if not g==f]
                    del data[f]
                    success=True
                else:
                    pass
        fp.close()
        num_done+=1
                
            
        
    

