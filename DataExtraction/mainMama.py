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


XS=[]
yS=[]
yS1=[]
XCT=[]



PathOfPatients = '\\\\PCCUBA\Fisica\PROYECTO PAYASO\\46Gy'
Algorithm = 'AAA'
Side = 'L'

PathOfPatients =os.path.join(os.path.join(PathOfPatients,Side),Algorithm)




cont=0
PatientList= os.listdir(PathOfPatients)
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

Results=[X,yS,yS1,XCT]

np.save('SetMama\\Data' + '-'+ Side  + '-' + Algorithm+ '.npy',Results)




















            
           