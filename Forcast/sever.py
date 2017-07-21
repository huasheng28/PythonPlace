# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 13:20:51 2017

@author: jgq
"""

#!/usr/bin/evn python
import socket
import signal
import errno


import numpy as np
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications.resnet50 import ResNet50

img_width, img_height = 224, 256

# predict result file
#output_file = '/home/jgq/Dande/DanDe/ResNet-on-Dande/output/keras_result10.txt'
# training weight path
#weights_path = '/home/jgq/Dande/DanDe/ResNet-on-Dande/output/weights_theano_test_gd.hdf5'


# predict result file
output_file = '/root/Dande/keras/output/keras_result10.txt'
# training weight path
weights_path = '/root/Dande/keras/output/weights_theano_test_31-2-8-5.hdf5'


batch_size = 1

base_model=ResNet50(include_top=False,weights=None)
x=base_model.output
x=GlobalAveragePooling2D()(x)
predictions=Dense(46,activation='softmax')(x)
model=Model(input=base_model.input,output=predictions)
model.compile(optimizer=SGD(lr=0.01, momentum=0.9, decay=1e-6),loss='categorical_crossentropy', metrics=['accuracy'])
model.load_weights(weights_path)

#info='/root/Dande/keras/data/predict/'
#filename='540.jpg'


def predict(items=None):
    
    #predict_path = '/home/jgq/Desktop/predict'
    with open(output_file,'w') as output:
        
        image_num=0
        while 1:
            image_batch=[]
            img = load_img(items, target_size=(img_width, img_height))
            image_batch.append(img_to_array(img))
            image_batch_num=len(image_batch)
            if image_batch_num % batch_size==0:
                break
              
        image_num+=len(image_batch)
            
        x_train = np.zeros((len(image_batch), 3,img_width, img_height), dtype="uint8")
        y_train=np.zeros(len(image_batch),dtype="uint8")
        for i,img in enumerate(image_batch):
            x_train[i,:,:,:]=img
        predict_datagen=ImageDataGenerator(rescale=1./255)
        predict_gengerator=predict_datagen.flow(x_train,y_train,shuffle=False,batch_size=batch_size)
            
                
        result=model.predict_generator(predict_gengerator,batch_size)
        result_val=result[0].argmax()+1
	p=result[0].max()

        if   (result_val==0 or result_val==1) and p>0.85:
            #return  1
            print 1
        elif (result_val==2 or result_val==3) and p>0.85:
            #return 2
            print 2
        elif result_val==4 and p>0.85:
            #return 3
            print 3
        elif (result_val==5 or result_val==6) and p>0.85:
            #return  4
            print 4
        elif result_val==7 and p>0.85:
            #return 5
            print 5
        elif (result_val==8 or result_val==9) or p<0.85 :
            #return  0
            print 0



def HttpResponse(header,whtml):
    f=file(whtml)
    contxtlist=f.readlines()
    context=''.join(contxtlist)
    response="%s %d\n\n%s\n\n"%(header,len(context),context)
    return response
    
def sigIntHander(signo,fram):
    print 'get signo#',signo
    global runflage
    runflage=False
    global lisfd
    lisfd.shutdown(socket.SHUT_RD)

          
#strHost="101.37.77.3"
strHost="192.168.1.104"
HOST=strHost
PORT=20014


httpheader = '''''\ 
HTTP/1.1 200 OK 
Context-Type: text/html 
Server: Python-slp version 1.0 
Context-Length: '''  


lisfd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#lisfd.setimeout(CHECK_TIMEOUT)
lisfd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
lisfd.bind((HOST,PORT))
lisfd.listen(50)

signal.signal(signal.SIGINT,sigIntHander)

runflag=True
while runflag:
    try:
        confd,addr=lisfd.accept()
       
    except socket.error as e:
        if e.errno==errno.EINTR:
            print 'get a except EINTR'
            
        else:
            raise
            
        continue
    
    if runflag==False:
        break
    print "connect by",addr
    
        
    data=confd.recv(1024)
    if not data:
        break
    print data
    
    #predict(items='/root/Dande/keras/data/predict/10165.jpg')
    predict(items='/home/jgq/Desktop/predict/1.jpg')
    confd.send(HttpResponse(httpheader,'index.html'))
    
    confd.close()
    
else:
    print 'runflag#',runflag
    
print 'Done'
    
    
    

