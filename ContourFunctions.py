# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 10:56:56 2018

@author: pgallego
"""
import numpy as np
#from GetDose import ReadContour, getDvh,GetMaskOfAPolygon
import scipy.misc
from matplotlib.path import Path
import matplotlib.pyplot as plt
  

def getCompleteContours(f,rd,ListOfIndex,Verbose):
    XC = [None]*len(ListOfIndex)
    YC = [None]*len(ListOfIndex)
    ZC = [None]*len(ListOfIndex)
    XXC= [None]*len(ListOfIndex)
           
    for i in range(len(ListOfIndex)):
        x,y,z ,X= GetStructCoord(f,rd ,ListOfIndex[i],Verbose) 
        XC[i] = x
        YC[i] =y
        ZC[i] =z
        XXC[i] =X
    return XC,YC,ZC,XXC 
                                
def GetStructCoord(file,rd, ContornoID,verbose = 0):

    RTV = file.ROIContourSequence[ContornoID]
    Ncortes = len(RTV.ContourSequence)

    x = []
    y = []
    z = []
    X = []
    for i in range(Ncortes):
        
        x0,y0,z0,X0 =  GetSliceCoords(RTV,rd,i)
        x=x+x0
        y=y+y0
        z=z+z0
        X=X+X0
               
   
#    if verbose ==1 : 
#        fig = plt.figure()
#        ax = fig.add_subplot(111, projection='3d')
#        
#        ax.scatter(x, y, z)
     
    return x,y,z,X

def GetSliceCoords(RTV,Rd,Slice):

        contours = [contour for contour in RTV.ContourSequence]
        
        position=(Rd.ImagePositionPatient)
        pixel=(Rd.PixelSpacing)
        Orientation=Rd.ImageOrientationPatient
        
        contour_coord = contours[Slice].ContourData
        x=[None]*int(len(contour_coord))
        y=[None]*int(len(contour_coord))
        X=[None]*int(len(contour_coord))   
        
        cx = contour_coord[0::3]
        
        cy = contour_coord[1::3]
       
        x = ((np.abs(float(position[0]))+float(Orientation[0])*np.array(cx))/float(pixel[0]))
        y=((np.abs(float(position[1]))+float(Orientation[4])*np.array(cy))/float(pixel[1]))
        z = contour_coord[2::3]
        X = list(zip(x,y))
      

#        for i in range(0, int(len(contour_coord)), 3):
#
#            
#            x[i]=((np.abs(float(position[0]))+float(Orientation[0])*contour_coord[i])/float(pixel[0]))
#            y[i]=((np.abs(float(position[1]))+float(Orientation[4])*contour_coord[i+1])/float(pixel[1]))
#        
#        
#            z[i]=( float(contour_coord[i + 2]))
#            X[i]=([x[-1],y[-1]])
#            #sX.append([float( contour_coord[i]), float(contour_coord[i + 1])])
#            cont = cont + 1
        return list(x),list(y),list(z),X
    
             
def GetMaskOfASlice(ListOfIndex, Slice,f,rd,pixelX,pixelY,XC,YC,ZC,XXC):
    MaskedImages =np.ndarray((len(ListOfIndex),pixelX,pixelY))
    cont2 = 0

    for i in ListOfIndex:
        
        X=[]
        x=[]
        y=[]
        z=[]

       # x,y,z ,X= GetStructCoord(f,rd ,i,x,y,z,X,Verbose)
  
    
        xb=np.array(XC[0])
        yb=np.array(YC[0])
        zb=np.array(ZC[0])

        
        x=np.array(XC[cont2])
        y=np.array(YC[cont2])
        z=np.array(ZC[cont2])
        X=np.array(XXC[cont2])  

        
        x =( x[z==Slice])*1.4-np.mean(xb[zb==Slice]*1.4) +pixelX/2
        y = (y[z==Slice])*1.4-np.mean(yb[zb==Slice]*1.4) +pixelY/2
        X= X[z==Slice]

        Lista =(list(map(lambda X: ((X[0]),(X[1])), list(zip(x,y)))))
        a = np.full((pixelX,pixelY), True, dtype=bool)

        if x!=[] and y!=[] :
            cosa= (GetMaskOfAPolygon(a,Lista) * a)
            cosa  = cosa.astype(np.float32)
          

            MaskedImages[cont2] = cosa#scipy.misc.imresize(cosa,(pixelX,pixelY) )
           
        else:
            cosa= np.full((pixelX,pixelY), False, dtype=bool)

            cosa  = cosa.astype(np.float32)

            MaskedImages[cont2] = cosa# scipy.misc.imresize(cosa,(pixelX,pixelY) )


        cont2=cont2+1
    return MaskedImages
   
    

def GetMaskOfAPolygon(Dosis,Polygon):
    
    x, y = np.meshgrid(np.arange(Dosis.shape[1]), np.arange(Dosis.shape[0])) # make a canvas with coordinates
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x,y)).T 

    p = Path(Polygon) # make a polygon
    grid = p.contains_points(points)
    mask = grid.reshape(Dosis.shape[0],Dosis.shape[1]) # now you have a mask with points inside a polygon
    
    return mask
