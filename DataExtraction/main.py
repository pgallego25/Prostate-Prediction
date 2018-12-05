# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 10:56:56 2018

@author: pgallego
"""
#import matplotlib.pyplot as plt
#from GetDose import ReadContour, getDvh,GetMaskOfAPolygon
#import time
import os
import numpy as np
from ReadPatientData import GetPatientData,SaveImages
from FindStructures import FindStructures
import time




input_shape=226
channels=3


XS=np.zeros((10000,input_shape,input_shape,channels))
yS=np.zeros((10000,20))
yS1=np.zeros((10000,20))

XCT=np.zeros((10000,input_shape,input_shape,1))
yDose=np.zeros((10000,input_shape,input_shape,1))


PathOfPatients= 'C:\\Users\\varian\\Desktop\\ProstatePrediction\\Patients\\SIB'
cont=0
#PatientList= [11] #TEST
PatientList= [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,101,102,103,104,106,107,109,110,112,114,115,116,117,118,119,120,121,122,123,125,126,127,128,129,131,132]

SliceConts=[]

Verbose = 0
start = time.time()

for i in range(len(PatientList)):

    print("Patient " + str(PatientList[i]) )
    PatientDir = os.path.join(PathOfPatients,str(PatientList[i]))

    ListOfIndex  = FindStructures(os.path.join(PatientDir,'Rs.dcm'))

    X,Listy,Xct,XDVH,CTList = GetPatientData(PatientDir,ListOfIndex,input_shape,input_shape,Verbose)

    SaveImages(i,X,Xct,XDVH,Listy,CTList,1)

    XS[cont:cont+X.shape[0],:,:,:]= X[:,:,:,:]
    yS[cont:cont+Listy[1].shape[0],:]=Listy[0][:,:]
    yS1[cont:cont+Listy[1].shape[0],:]=Listy[0][:,:]
    XCT[cont:cont+Xct.shape[0],:,:,0]= Xct[:,:,:]
   # yDose[cont:cont+Dosis.shape[0],:,:,:]= Dosis[:,:,:,:]
    
    
    cont=cont+X.shape[0]
    SliceConts.append(cont)
end = time.time()
print(end - start)


XS= XS[0:cont,:,:,:]
yS= yS[0:cont,:]
yS1= yS1[0:cont,:]
XCT= XCT[0:cont,:,:,:]
#yDose= yDose[0:cont,:,:,:]

np.save('XS.npy',XS)
np.save('yS.npy',yS)
np.save('yS1.npy',yS1)
np.save('XCT.npy',XCT)




















            
           