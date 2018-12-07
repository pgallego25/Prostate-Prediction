# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 10:41:46 2018

@author: Varian
"""
import numpy as np


def PrepareData(N,N2):
    
    
    XS = np.load('Data\XS.npy')
    yS = np.load('Data\YS.npy')
    Slices = np.load('Data\SliceConts.npy')
    yN=np.zeros((yS.shape[0],yS.shape[1]))
    for i in range((yS.shape[0])):
        if yS[i,0]==0: 
            yN[i] = yS[i]
        else:   
            yN[i]=  yS[i] / yS[i,0]
    
    Corte1 = int(N*len(Slices))
    Corte2 = Corte1 + int(N2*len(Slices))
    
    
    X_train=XS[0:Slices[Corte1],:,:,:]
    y_train=yN[0:Slices[Corte1],:] 
    
    X_val=XS[Slices[Corte1]:Slices[Corte2],:,:,:]
    y_val=yN[Slices[Corte1]:Slices[Corte2],:]
      
    X_test=XS[Slices[Corte2]:,:,:,:]
    y_test=yN[Slices[Corte2]:,:]
    
    
    
    return X_train,y_train,X_val,y_val,X_test,y_test,Slices[0:Corte1],Slices[Corte1:Corte2],Slices[Corte2:]

