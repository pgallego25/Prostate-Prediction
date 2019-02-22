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


###MAMA
PathOfPatients = '\\\\PCCUBA\Fisica\PROYECTO PAYASO'

DoseList=['50Gy','46Gy']
AlgoList = ['AAA','PBC']
SideList = ['R','L']

for Dose in DoseList:
    for Algorithm in AlgoList:
        for Side in SideList:
                        
            XS=[]
            yS=[]
            yS1=[]
            XCT=[]
            NHC = []
            PathOfPatients = '\\\\PCCUBA\Fisica\PROYECTO PAYASO'
            PathOfPatients =os.path.join(PathOfPatients,Dose)
            PathOfPatients =os.path.join(os.path.join(PathOfPatients,Side),Algorithm)
            print(PathOfPatients)
            
            ###Prostata
            """
            PathOfPatients = 'C:\\Users\\Varian\\Desktop\\ProstatePrediction\\Patients\\SuperTest'
            Side='P'
            Dose=''
            Algorithm = 'prostate'
            """
            
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
                if Side=='P':
                    ListOfIndex  = FindStructures(os.path.join(PatientDir,Rs))
                else:   
                    ListOfIndex  = FindStructuresBreast(os.path.join(PatientDir,Rs),Side)
            
                try:
                    X,Listy,Xct,XDVH,CTList,nhc = GetPatientData(PatientDir,ListOfIndex,input_shape,input_shape,Side,Verbose)
                    
                    plt.show()
                    SaveImages(PatientList[i],X,Xct,XDVH,Listy,CTList,1,10)
                    NHC.append(nhc)
                    XS.append(X[:,:,:,:])
                    yS.append(Listy[0][:,:])
                    yS1.append(Listy[1][:,:])
                    XCT.append( Xct[:,:,:])
                except:
                    print("El paciente " + str(PatientList[i]) + " no se ha podido importar")
               # yDose[cont:cont+Dosis.shape[0],:,:,:]= Dosis[:,:,:,:]
                
                
            end = time.time()
            print(end - start)
            
            Results=[X,yS,yS1,XCT,NHC]

            np.save('SetMama\\Data' + '-'+ Side  + '-' + Algorithm+ '-'+Dose+ '.npy',Results)




















            
           