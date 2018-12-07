# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 14:04:20 2018

@author: pgallego
"""

from keras.callbacks import TensorBoard,ModelCheckpoint
from VGG16.vgg16 import CreateModel
from VGG16.PrepareData import PrepareData
from VGG16.Evaluate import evaluate
import os


input_shape=226
channels=3




X_train,y_train,X_val,y_val,X_test,y_test,SCtrain,SCval,SCtest = PrepareData(0.8,0.1)

logdir= "Graph"
Rundir="Test"


logPath = os.path.join(logdir,Rundir)
checkpointcallback = ModelCheckpoint(os.path.join(logPath,'BestModel'),
                monitor='val_loss', verbose=0, save_best_only=True,
                save_weights_only=True, mode='auto', period=1)
tbCallback = TensorBoard(log_dir=logPath, histogram_freq=0,
                            write_graph=True, write_images=True)

    
   

model = CreateModel(input_shape,input_shape,channels,logdir,Rundir,20)



for i in range(1000):
    
    model.fit(X_train[0:100],y_train[0:100],batch_size=1, 
              callbacks=[tbCallback,checkpointcallback],epochs=1,shuffle=True)
    
#    
#    N = 20
#    plt.plot(y_test[N])
#    ys=model.predict(X_test[N:N+1])
#    plt.plot(ys[0,:])
#    plt.show()
    #model.load_weights(logdir+Rundir+'\\BestModel3')
    a,b = evaluate(X_test,y_test,SCtest,model,1,1) 
    print(a)
    print(b)
      
    
