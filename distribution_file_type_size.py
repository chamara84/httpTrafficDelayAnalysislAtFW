import re
import string

__author__="Chamara"
__date__ ="$Mar 30, 2012 2:21:55 PM$"


import csv





def main():
    fileName = 'C:\\Documents and Settings\\umdevana\\My Documents\\Python_scripts\\logs\\logs\\http_responses_anon.csv'
    file = open(fileName,'rb')
    timestamps={}
    text_fsize = [];
    image_fsize = [];
    video_fsize = [];
    executable_fsize = [];
    unknown_fsize = [];
    animation_fsize = [];
    compressed_fsize =[];
    documents_fsize = [];
    script_fsize = [];
    fsize_names = ['text_fsize','image_fsize','video_fsize','executable_fsize',\
                    'script_fsize','documents_fsize','animation_fsize','compressed_fsize',\
                    'unknown_fsize']
    namesOfTypes = ['text','image','video','executable','script',\
                    'documents','animation','compressed','unknown'];

    #text parameters
    textExt = ['jhtml','htm','tex','txt','html','css','rss','orig','shtml',\
                'xml','rdf','wml','wtf','pkix-crl','ocsp-response','plain','rss+xml','cross-domain-policy']
    Number_text= [0,0]; #index 0 contains ones with no content encoding index 1 has gzip
    #image parameters
    imageExt = ['jpg','ico','gif','ps','gallery','png','PNG','jpeg','JPG','icon','bmp']
    Number_image= [0,0];

    #video parameters
    videoExt = ['ogg','flv','amf','mp4','fcs']
    Number_video= [0,0];

    #executable parameters
    executableExt = ['do','exe','action','octet-stream']
    Number_executable= [0,0];

    #script parameters
    scriptExt = ['cfm','py','json','cgi','phtml','asp','js','jsp','php',\
                'ashx','axd','gne','aspx','dll','jspx','javascript']
    Number_script= [0,0];

    #unknown parameters
    unknownExt = set([])
    Number_unknown= [0,0];

    #document parameters
    documentsExt = ['g','pdf','msword',]
    Number_documents= [0,0];

    #animation parameters
    animationExt = ['swf','shockwave-flash']
    Number_animation= [0,0];

    #compressed parameters
    compressedExt = ['rar','zip','gzip','bzip2']
    Number_compressed= [0,0];

    types = [textExt,imageExt,videoExt,executableExt,scriptExt,\
            documentsExt,animationExt,compressedExt,unknownExt]

    lines=list(csv.reader(file))
    contenType_column=lines[0].index('content-type')
    encodingType_column=lines[0].index('content-encoding')
    length_column=lines[0].index('content-length')


    for line in lines[1:]:
        contentStr=line[contenType_column].split('/')[-1]
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
                vars()[fsize_names[index_fsize_names]].append(line[length_column])
                if line[encodingType_column]in ['','none']:
                    count_name = 'Number_'+namesOfTypes[index_fsize_names]
                    vars()[count_name][0] += vars()[count_name][0]
                    break
                elif line[encodingType_column] in ['gzip','sdch,gzip','deflate','x-gzip']:
                    vars()[count_name][1] += vars()[count_name][1]
                    break

                else:
                    print 'ContentType:'+line[encodingType_column]
                    break

            elif index_fsize_names == 8:
                unknownExt.add(contentStr)
                break
                

    file = open('C:\\Documents and Settings\\umdevana\\My Documents\\Python_scripts\\logs\\unknown.txt','wb')
    for ext in unknownExt:
        file.write(ext+'\n')
     
    file.close()

    for name in fsize_names:
        file = open('C:\\Documents and Settings\\umdevana\\My Documents\\Python_scripts\\logs\\'+name+'.txt','wb')
        for size in vars()[name]:
            if size =='':
                file.write('0'+'\n')
            else:
                file.write(size+'\n')

        file.close()


    



if __name__ == "__main__":
    main()