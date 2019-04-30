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
import pandas as pd


input_shape=226
channels=3





###MAMA
Path = 'C:\\github\\Prostate-Prediction\\Data'
AlgoList = ['AAA','PBC']
SideList = ['L','R']
Folder= 'SetMama'


###Prostata
Path= 'C:\\github\\Prostate-Prediction\\DataNew'
DoseList=['SIB']
AlgoList = ['Prostate']
SideList = ['P']
Folder= 'SetProstata'


PatientList= os.listdir(Path)


#Excel = pd.read_excel('AnalisisBienHecho.xlsx',index_col = 1,header = None)

WrongPatients=[]

for Algorithm in AlgoList:
    for Side in SideList:
        print('Leyendo pacientes de mama ' + Side +' algoritmo ' + Algorithm)
        XS=[None]*200
        yS=[None]*200
        yS1=[None]*200
        XCT=[None]*200
        NHC = [None]*200
        DoseList=[None]*200
        cont = 0
        Verbose = 0
        for i in range(len(PatientList)):

         #   nhcfolder = Excel.loc[float(PatientList[i])]
            
        #    if nhcfolder[7]==Side and nhcfolder[8]==Algorithm:
            PatientDir = os.path.join(Path,str(PatientList[i]))
            print(PatientDir)
            print(str(cont) + '/' + str(len(PatientList)))
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
    
               
              #  SaveImages(PatientList[i],X,Xct,XDVH,Listy,CTList,1,10,nhc)
       
                XS[cont] = (X[:,:,:,:])
                yS[cont] =(Listy[0][:,:])
                yS1[cont] =(Listy[1][:,:])
                XCT[cont] =( Xct[:,:,:])
                NHC[cont] =( nhc)
       
             #   DoseList[cont] =(nhcfolder[9])
                cont=cont+1

            except:
                WrongPatients.append(PatientList[i])
                print("El paciente " + str(PatientList[i]) + " no se ha podido importar")
           # yDose[cont:cont+Dosis.shape[0],:,:,:]= Dosis[:,:,:,:]

        XS = XS[0:cont]
        yS = yS[0:cont]
        yS1 = yS1[0:cont]
        XCT = XCT[0:cont]
        NHC = NHC[0:cont]

      #  DoseList = DoseList[0:cont-1]
        #Results=[XS,yS,yS1,NHC,DoseList]
        Results=[XS,yS,yS1,NHC]
        print("Saving : "+'\\DataNew' + '-'+ Side  + '-' + Algorithm+ '-'+ '.npy')
        np.save(Folder + '\\DataNew' + '-'+ Side  + '-' + Algorithm+ '-'+ '.npy',Results)



















            
           