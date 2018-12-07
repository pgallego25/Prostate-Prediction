# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 14:04:20 2018

@author: pgallego
"""

from keras.callbacks import TensorBoard,ModelCheckpoint
from VGG16.vgg16 import CreateModel
from VGG16.PrepareData import PrepareData
from VGG16.Evaluate import evaluate
from VGG16.CheckPatientDVH import checkdvh
import os




##Prepare data 
X_train,y_train,X_val,y_val,X_test,y_test,SCtrain,SCval,SCtest = PrepareData(0.8,0.1)
Rundir="Test"
logPath = os.path.join("Graph",Rundir)

##Callbacks for model
checkpointcallback = ModelCheckpoint(os.path.join(logPath,'BestModel'),
                monitor='val_loss', verbose=0, save_best_only=True,
                save_weights_only=True, mode='auto', period=1)
tbCallback = TensorBoard(log_dir=logPath, histogram_freq=0,
                            write_graph=True, write_images=True)
     
##Create Model 
input_shape=226
channels=3
model = CreateModel(input_shape,input_shape,channels,20)

##Fit the model and evaluate complete patients. 
for i in range(1000):
    
    model.fit(X_train,y_train,batch_size=1, 
              callbacks=[tbCallback,checkpointcallback],epochs=1,shuffle=True)

    #model.load_weights(logdir+Rundir+'\\BestModel3')
    a,b = evaluate(X_train,y_train,SCtrain,model,10,1)  #PENDIENTE DE ARREGLAR PARA TEST Y VAL.
   # a,b = checkdvh(X_train,y_train,SCtrain,model,10,1) 

    print(a)
    print(b)
      
    
    
    
