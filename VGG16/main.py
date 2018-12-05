# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 14:04:20 2018

@author: pgallego
"""

import numpy as np
from keras.callbacks import TensorBoard,ModelCheckpoint
from vgg16 import CreateModel
from PrepareDate import PrepareData
import os


input_shape=226
channels=3




X_train,y_train,X_val,y_val,X_test,y_test = PrepareData(0.8,0.1)

logdir= "Graph"
Rundir="Test"
logPath = os.path.join(logdir,Rundir)
checkpointcallback = ModelCheckpoint(os.path.join(logPath,'BestModel'), monitor='val_loss', verbose=0, save_best_only=True, save_weights_only=True, mode='auto', period=1)
tbCallback = TensorBoard(log_dir=logdir+Rundir, histogram_freq=0,
                            write_graph=True, write_images=True)

    
   

model = CreateModel(input_shape,input_shape,channels,logdir,Rundir,20)

model.fit(X_train,y_train,batch_size=1,validation_data=(X_val,y_val), callbacks=[tbCallback,checkpointcallback],epochs=10000,shuffle=True)

model.load_weights(logdir+Rundir+'\\BestModel3')


#model.evaluate(XS[0:2672,:,:,:],yS[0:2672,:])
#model.evaluate(XS[2672:2682,:,:,:],yS[2672:2682,:])
#model.evaluate(XTest,yTest[:,0:20])



