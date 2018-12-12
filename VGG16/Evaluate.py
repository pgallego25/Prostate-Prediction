# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 08:52:37 2018

@author: Varian
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 12:51:08 2018

@author: Varian
"""
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt



def evaluate(X,y,SC,model,bucle,verbose = 0) :   
    SC2 = SC[1:]-SC[:-1]
    SliceConts = [0]*len(SC)
    for i in range(len(SliceConts))[1:]:
        SliceConts[i-1] = np.sum(SC2[0:i])
    SliceConts[-1]= np.sum(SC)
    SliceConts=np.concatenate(([0],SC2))
    print(SliceConts)
    a=0
    b=0
    print( SliceConts)
    for i in range(bucle):#range(len(SliceConts)-1):
        
        print('Analizing Patient ' + str(i) + '/'+ str(len(SliceConts)-1))
        Min=0
        Max=80 
        Pasos= 20
        Rango = np.arange(Min,Max, (Max-Min)/Pasos)
        
        yt = np.sum(np.array(y[SliceConts[i]:SliceConts[i+1],:]),axis = 0 ) 
        ym=  np.sum(model.predict(X[SliceConts[i]:SliceConts[i+1],:,:,:]),axis = 0)


        if verbose ==1:
            print (i)
            plt.plot(Rango,yt/yt[0],color='red',marker='o',linestyle='--')  
            plt.plot(Rango,ym/yt[0],color='blue',marker='o',linestyle='--')     
            plt.grid(True)
            plt.title("Rectum DVH")
            plt.show()
            
      
        a = a +1/len(ym)*np.mean(np.power(yt-ym,2))
        b=b+1/len(ym)*np.mean(np.abs(yt-ym))
        
        
     
        
        
    if verbose ==2:
        for i in range(bucle):#range(len(SliceConts)-1):

        #for i in range(len(SliceConts)-1):
            print('Analizing Patient ' + str(i) + '/'+ str(len(SliceConts)-1))
            ym=  np.sum(model.predict(X[SliceConts[i]:SliceConts[i+1],:,:,:]),axis = 0)
            plt.plot(Rango,ym,color='blue',marker='o',linestyle='--')
            
        plt.savefig('all.png')
        plt.show()    
    return a,b