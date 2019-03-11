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




###Prostata
Path= 'C:\\Users\\varian\\Desktop\\ProstatePrediction\\Patients\\SIB'
DoseList=['SIB']
AlgoList = ['Prostate']
SideList = ['P']
Folder= 'SetProstata'


###MAMA
Path = '\\\\PCCUBA\Fisica\PROYECTO PAYASO\\NEW'
AlgoList = ['PBC','AAA']
SideList = ['L','R']
Folder= 'SetMama'

PatientList= os.listdir(Path)

cont = 0

Excel = pd.read_excel('AnalisisBienHecho.xlsx',index_col = 1,header = None)

WrongPatients=[]

for Algorithm in AlgoList:
    for Side in SideList:
        print('Leyendo pacientes de mama ' + Side +' algoritmo ' + Algorithm)
        XS=[]
        yS=[]
        yS1=[]
        XCT=[]
        NHC = []
        DoseList=[]
 
        SliceConts=[]
        Verbose = 0
        
        for i in range(len(PatientList)):
        
            nhcfolder = Excel.loc[float(PatientList[i])]
            if nhcfolder[7]==Side and nhcfolder[8]==Algorithm:
                PatientDir = os.path.join(Path,str(PatientList[i]))
                print(PatientDir)
                print(str(cont) + '/' + str(len(PatientList)))
                cont=cont+1
                for j in os.listdir(PatientDir):
                    if re.search('RS', j, re.IGNORECASE):
                        
                       Rs = j
                       break
                try:
                    if Side=='P':
                        ListOfIndex  = FindStructures(os.path.join(PatientDir,Rs))
                    else:   
                        ListOfIndex  = FindStructuresBreast(os.path.join(PatientDir,Rs),Side)
            
                
                    X,Listy,Xct,XDVH,CTList,nhc = GetPatientData(PatientDir,ListOfIndex,input_shape,input_shape,Side,Verbose)
                    
                    plt.show()
                    SaveImages(PatientList[i],X,Xct,XDVH,Listy,CTList,1,10,nhc)
                    NHC.append(nhc)
                    XS.append(X[:,:,:,:])
                    yS.append(Listy[0][:,:])
                    yS1.append(Listy[1][:,:])
                    XCT.append( Xct[:,:,:])
                    DoseList.append(nhcfolder[9])
                except:
                    WrongPatients.append(nhcfolder)
                    print("El paciente " + str(PatientList[i]) + " no se ha podido importar")
               # yDose[cont:cont+Dosis.shape[0],:,:,:]= Dosis[:,:,:,:]
            
     
            
            Results=[XS,yS,yS1,XCT,NHC,DoseList]

            np.save(Folder + '\\Data' + '-'+ Side  + '-' + Algorithm+ '-'+ '.npy',Results)




















            
           