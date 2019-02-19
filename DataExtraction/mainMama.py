# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 16:26:32 2019

@author: Varian
"""

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
from FindStructures import FindStructures,FindStructuresBreast
import time
import re
import matplotlib.pyplot as plt


input_shape=226
channels=3


XS=[]#np.zeros((10000,input_shape,input_shape,channels))
yS=[]#np.zeros((10000,20))
yS1=[]#np.zeros((10000,20))
XCT=[]#np.zeros((10000,input_shape,input_shape,1))



PathOfPatients = '\\\\PCCUBA\Fisica\PROYECTO PAYASO\\46Gy'
Algorithm = 'AAA'
Side = 'L'

PathOfPatients =os.path.join(os.path.join(PathOfPatients,Side),Algorithm)




cont=0
#PatientList= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,101,102,103,104,106,107,109,110,112,114,115,116,117,118,119,120,121,122,123,125,126,127,128,129,131,132]
#PatientList= [1,2]
PatientList= os.listdir(PathOfPatients)#[34]

SliceConts=[]
Verbose = 0
start = time.time()

for i in range(len(PatientList)):

    print("Patient " + str(PatientList[i]) )
    PatientDir = os.path.join(PathOfPatients,str(PatientList[i]))


    for j in os.listdir(PatientDir):
        if re.search('RS', j, re.IGNORECASE):
            
           Rs = j
           break
 #   ListOfIndex  = FindStructures(os.path.join(PatientDir,Rs))
    ListOfIndex  = FindStructuresBreast(os.path.join(PatientDir,Rs),Side)


    X,Listy,Xct,XDVH,CTList = GetPatientData(PatientDir,ListOfIndex,input_shape,input_shape,Verbose)

    
    plt.show()
    SaveImages(PatientList[i],X,Xct,XDVH,Listy,CTList,1,10)

    XS.append(X[:,:,:,:])
    yS.append(Listy[0][:,:])
    yS1.append(Listy[1][:,:])
    XCT.append( Xct[:,:,:])
   # yDose[cont:cont+Dosis.shape[0],:,:,:]= Dosis[:,:,:,:]
    
    
    cont=cont+X.shape[0]
end = time.time()
print(end - start)


XS= XS[0:cont,:,:,:]
yS= yS[0:cont,:]
yS1= yS1[0:cont,:]
XCT= XCT[0:cont,:,:,:]
#yDose= yDose[0:cont,:,:,:]

np.save('SetMama\\X' + '-'+ Side  + '-' + Algorithm+ '.npy',XS)
np.save('SetMama\\y' + '-'+ Side  + '-' + Algorithm+ '.npy',yS)
np.save('SetMama\\XCT' + '-'+ Side  + '-' + Algorithm+ '.npy',XCT)





















            
           