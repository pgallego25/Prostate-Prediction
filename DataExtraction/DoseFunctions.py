# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 10:47:27 2018

@author: pgallego
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from ContourFunctions import GetSliceCoords
import scipy.misc

def GetStructCoordPlusDVH(file,rd, ContornoID,pixelX,pixelY,verbose = 0):

    # handle `/` missing
   # f = dicom.read_file('C:\\TestNet\\RS.1.2.246.352.71.4.715124098882.112695.20180801082024.dcm')
   
        
    RTV = file.ROIContourSequence[ContornoID]
    Ncortes = len(RTV.ContourSequence)

    xdvh=[]
    ydvh=[]
    zdvh=[]
    Xdvh=[]
    Z=[]
    y_dvh=[None]*Ncortes
    DoseSlice = np.zeros((Ncortes,pixelX,pixelY))

    NonCeroPoints=[None]*Ncortes
    for i in range(Ncortes):
        xdvh.clear()
        ydvh.clear()
        zdvh.clear()
        Xdvh.clear()
        xdvh,ydvh,zdvh,Xdvh = GetSliceCoords(RTV,rd,i)
#        plt.plot(xdvh,ydvh)
#        plt.show()

        x_dvh, y_dvh[i],NonCeroPoints[i],Dose = getDvh(Xdvh,zdvh[0],rd,xdvh,ydvh,verbose)

        Z.append(zdvh[0])

        DoseSlice[i]=scipy.misc.imresize(Dose,(pixelX,pixelY) )

#    if verbose ==1 : 
#        fig = plt.figure()
#        ax = fig.add_subplot(111, projection='3d')
#        
#        ax.scatter(x, y, z)

        
    
    return x_dvh,y_dvh,Z,DoseSlice


def getSliceDose(Rd,Slice):
   # print(Slice)
    matrix = Rd.pixel_array
    
    ListaCortes = np.round((np.array(Rd.GridFrameOffsetVector)) + float(Rd.ImagePositionPatient[2]),1)
    #print(ListaCortes)
     #print(np.round(Slice,1))
   #  print(np.sum(ListaCortes == np.round(Slice,1)))
    if np.sum(ListaCortes == np.round(Slice,1)) == 0:
        print("No hay coincidencias")
    else:
        Output = matrix[ListaCortes ==  np.round(Slice,1),:,:]
        #plt.imshow(Output[0])   
        #plt.show()
    return Output[0]

def GetMaskOfAPolygon(Dosis,Polygon):
    
    x, y = np.meshgrid(np.arange(Dosis.shape[1]), np.arange(Dosis.shape[0])) # make a canvas with coordinates
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x,y)).T 

    p = Path(Polygon) # make a polygon
    grid = p.contains_points(points)
    mask = grid.reshape(Dosis.shape[0],Dosis.shape[1]) # now you have a mask with points inside a polygon
    
    return mask

def getDvh(X,ZSlicePos,Rd,x,y,Verbose = 0):
    Output = getSliceDose(Rd,ZSlicePos)*Rd.DoseGridScaling
    
   # plt.show()
    maskedImage = GetMaskOfAPolygon(Output,X) * Output


#    plt.imshow(maskedImage)
#    plt.show()
   
    NonCeroPoints = np.count_nonzero(maskedImage)       
    Min=0
   # Max=80 #np.max(maskedImage)+ 0.15 * np.max(maskedImage)
    Max=80 #np.max(maskedImage)+ 0.15 * np.max(maskedImage)
    Pasos= 20
    Rango = np.arange(Min,Max, (Max-Min)/Pasos)
    
    DvhPoints= []
    for i in range(len(Rango)):
         mask_output2 = (maskedImage >= Rango[i])*maskedImage
         DvhPoints.append(np.count_nonzero(mask_output2) )
         
    if Verbose ==1:
        plt.figure()
        
        plt.subplot(2, 1, 1)
        plt.plot(Rango, DvhPoints, 'o-')
        plt.title('Image + Slice Rectum DVH')
        plt.ylabel('nº Pixels')
        
        plt.subplot(2, 1, 2)
        plt.scatter(x,y)
        plt.imshow(Output)
 
        
        plt.show()


    return Rango,DvhPoints,NonCeroPoints,Output