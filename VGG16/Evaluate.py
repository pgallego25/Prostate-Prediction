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



def evaluate(X,y,SC,model,logdir,Rundir,verbose = 0) : 
  
       
    
    SC = SC - SC[0]
    SliceConts=SC
    a=0
    b=0
    
    for i in range(len(SliceConts)-1):
        Min=0
        Max=80 #np.max(maskedImage)+ 0.15 * np.max(maskedImage)
        Pasos= 20
        Rango = np.arange(Min,Max, (Max-Min)/Pasos)
        
        DvhRecto = np.sum(np.array(y[SliceConts[i]:SliceConts[i+1],0:20]),axis = 0 ) 
        DvhRectoN = DvhRecto/DvhRecto[0]# / DvhRecto[0]  
        if verbose ==1:
            print (i)
            plt.plot(Rango[0:20],DvhRectoN[0:20],color='red')  
            plt.scatter(Rango[0:20],DvhRectoN[0:20],color='red')
            plt.grid()
            plt.title("Rectum DVH")
               
        ys= model.predict(X[SliceConts[i]:SliceConts[i+1],:,:,:])
        
        Min=0
        Max=80 #np.max(maskedImage)+ 0.15 * np.max(maskedImage)
        Pasos= 20
        Rango = np.arange(Min,Max, (Max-Min)/Pasos)
        
        DvhRecto2 = np.sum(np.array(ys[:,:]),axis = 0 ) 
        DvhRecto2N = DvhRecto2/DvhRecto[0]# / DvhRecto2[0]  *  DvhRecto[10]    - DvhRecto2[-1] / DvhRecto2[0]  *  DvhRecto[10] 
        DvhRecto2N = DvhRecto2N - DvhRecto2N[-1]
        if verbose ==1:

            plt.plot(Rango[0:20],DvhRecto2N,color='blue')     
            plt.scatter(Rango[0:20],DvhRecto2N,color='blue')   
            plt.grid()
            plt.title("Rectum DVH")
            plt.savefig(str(i) + 'Test.png')       
            plt.show()
            
      
        a = a +1/len(ys)*np.mean(np.power(DvhRecto[0:20]-DvhRecto2,2))
        b=b+1/len(ys)*np.mean(np.abs(DvhRecto[0:20]-DvhRecto2))
        
        
     
        
        
    if verbose ==1:
    
        for i in range(len(SliceConts)-1):
           
           # model= load_model('ModelosGuardadosRecto/BestModelRectum')
            ys= model.predict(X[SliceConts[i]:SliceConts[i+1],:,:,:])
                
            Min=0
            Max=80 #np.max(maskedImage)+ 0.15 * np.max(maskedImage)
            Pasos= 20
            Rango = np.arange(Min,Max, (Max-Min)/Pasos)
            DvhRecto = np.sum(np.array(y[SliceConts[i]:SliceConts[i+1],0:20]),axis = 0 ) 
        
            DvhRecto2 = np.sum(np.array(ys[:,:]),axis = 0 ) 
            DvhRecto2 = DvhRecto2 /DvhRecto[0]
            plt.plot(Rango[10:20],DvhRecto2,color='blue')     
            plt.scatter(Rango[10:20],DvhRecto2,color='blue')
            plt.savefig('all.png')
    return a,b