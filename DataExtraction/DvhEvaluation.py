# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:49:19 2019

@author: Varian
"""
import numpy as np

PathOfPatients = 'C:\\Users\\Varian\\Desktop\\ProstatePrediction\\Patients\\SuperTest'
Side='L'
Dose='50Gy'
Algorithm = ['AAA','PBC']


Min=0
Max=60 
Pasos= 20
Rango = np.arange(Min,Max, (Max-Min)/Pasos)


V20AAA = []
V20PBC = []


SideList = ['L']
Dose='50Gy'

for Side in SideList:
    PulmonLAAA = np.load('Data' + '-'+ Side  + '-' + 'AAA'+ '-'+Dose+ '.npy')[1]
    CorLAAA = np.load('Data' + '-'+ Side  + '-' + 'AAA'+ '-'+Dose+ '.npy')[2]
    
    PulmonLPBC = np.load('Data' + '-'+ Side  + '-' + 'PBC'+ '-'+Dose+ '.npy')[1]
    
    CorLPBC = np.load('Data' + '-'+ Side  + '-' + 'PBC'+ '-'+Dose+ '.npy')[2]
    
    #V21 approx el punto 7
    
    
    for i in CorLAAA:
        suma = np.sum(i,axis= 0)
        print(suma)
        V20AAA.append(suma[8]/suma[0])
        
    
    for i in CorLPBC:
        suma = np.sum(i,axis= 0)
        print(suma)
        V20PBC.append(suma[8]/suma[0])
        
    import matplotlib.pyplot as plt
    

plt.hist(V20AAA)

plt.show()


plt.hist(V20PBC)

plt.show()

print(np.mean(V20AAA))
print(np.std(V20AAA))

print(np.mean(V20PBC))
print(np.std(V20PBC))