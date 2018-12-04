# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 13:00:25 2018

@author: Varian
"""
import os
import numpy as np
import pydicom as dicom
from ContourFunctions import getCompleteContours,GetMaskOfASlice
import scipy.misc
import matplotlib.pyplot as plt
from DoseFunctions import GetStructCoordPlusDVH


def GetPatientData(PatientDir,ListOfIndex,input_shape,input_shape2,Verbose = 0):
        YDVH,XDVH,ZDVH,DOSESLICE = ReadDVHOnePatient(PatientDir,ListOfIndex,input_shape,input_shape,0)
        Zlist = (set(ZDVH[1]+ZDVH[2])) 
        Xct,XUnsorted, CTList = ReadCtOnePatient(PatientDir,ListOfIndex,input_shape,input_shape,Zlist,Verbose)
        
        
        CTList = (np.array(CTList))
        
        Indices = np.argsort(CTList)
        
        
        y = np.zeros((len(CTList),20))
        
        listOfYs=[]
            
        for d in range(len(YDVH))[1:]:
            for c in range(len(CTList)):
    
                if CTList[c] in ZDVH[d]:
                    Position = ZDVH[d].index(CTList[c])
                    y[c,:] = YDVH[d][Position]
                else:
                    y[c,:] = np.zeros((1,20))
            listOfYs.append(y[Indices])
        return XUnsorted[Indices],listOfYs,Xct[Indices],XDVH,CTList[Indices]




def ReadCtOnePatient(PatientDir,ListOfIndex,pixelX,pixelY,Zlist,Verbose=0):
    ##Getting paths and reading Dose and structure files. 
    
    Rspath = os.path.join(PatientDir, 'Rs.dcm')
    RdPath = os.path.join(PatientDir, 'Rd.dcm')
    f = dicom.read_file(Rspath,force=True)
    rd =  dicom.read_file(RdPath,force=True)
    rd.file_meta.TransferSyntaxUID = dicom.uid.ImplicitVRLittleEndian
   
    ##Reading list of CT Images. 
    dirs = os.listdir(PatientDir)
    CTlist=[]
    cont=0
    
    #Generating Zero outputs. 
    Xm = np.zeros((len(dirs),pixelX,pixelY,3))
    XCT = np.zeros((len(dirs),pixelX,pixelY))
    
    
    #Contour matrix: Read and generate contours included in ListOfIndex
    XC,YC,ZC,XXC = getCompleteContours(f,rd,ListOfIndex,Verbose)
   
    #Reading each Image CT file and creating  masks.
    for i in dirs:
        if 'image' in i:

            Img = dicom.read_file(os.path.join(PatientDir,i),force =True)
        #    print('Getting Slice: ' + str(Img.SliceLocation))
            if Img.SliceLocation in Zlist:
                CTlist.append(float(Img.SliceLocation))    
    
                
                rd.file_meta.TransferSyntaxUID = dicom.uid.ImplicitVRLittleEndian                    
                Img.file_meta.TransferSyntaxUID = dicom.uid.ImplicitVRLittleEndian            
                CtImage=scipy.misc.imresize(Img.pixel_array,(pixelX,pixelY) )
    
               
                if Verbose==1:
                    print(Img.SliceLocation)
                    plt.imshow(CtImage)
                    plt.show()
    
                MaskedImages  = GetMaskOfASlice(ListOfIndex, float(Img.SliceLocation),f,rd,pixelX,pixelY,XC,YC,ZC,XXC)
    
                XCT[cont,:,:] = CtImage            
                
                Xm[cont,:,:,0] = (MaskedImages[3]+MaskedImages[4]+MaskedImages[5])*100 ++MaskedImages[6]*1000
                Xm[cont,:,:,1] = (MaskedImages[1]*10+MaskedImages[2]*50)
                Xm[cont,:,:,2] = MaskedImages[0]
               
                if Verbose==1:
                    plt.imshow(Xm[cont,:,:,0:3])
                    plt.show()
                cont=cont +1 
               
    Xm = Xm[0:cont,:,:,:]
    XCT = XCT[0:cont,:,:]
    return XCT,Xm,CTlist


def ReadDVHOnePatient(PatientDir,ListOfIndex,pixelX,pixelY,Verbose=0):
    Rspath = os.path.join(PatientDir, 'Rs.dcm')
    RdPath = os.path.join(PatientDir, 'Rd.dcm')
    f = dicom.read_file(Rspath,force=True)
    rd =  dicom.read_file(RdPath,force=True)
    rd.file_meta.TransferSyntaxUID = dicom.uid.ImplicitVRLittleEndian
   
    ##Reading list of CT Images. 
    

    XDVH = [None]*len(ListOfIndex)
    YDVH = [None]*len(ListOfIndex)
    ZDVH = [None]*len(ListOfIndex)
    DOSESLICE =[None]*len(ListOfIndex) 
    for l in range(len(ListOfIndex))[1:]:

        XDVH[l],YDVH[l],ZDVH[l],DOSESLICE[l] = GetStructCoordPlusDVH(f,rd ,ListOfIndex[l],pixelX,pixelY,Verbose)
    
    return YDVH,XDVH,ZDVH,DOSESLICE

    

def SaveImages(i,X,Xct,XDVH,Listy,CTList,Verbose): 
    if Verbose == 1:
        N =26
           
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
      
        ax1.imshow(X[N,:,:,:])
    
        ax2.imshow(Xct[N,:,:])
        ax2.set_title('CT')
        
        ax3.plot(XDVH[1],Listy[0][N,:])
        ax3.set_title('Recto DVH')
        
        
        
        ax4.plot(XDVH[1],Listy[1][N,:])
        ax4.set_title('Vejiga DVH')
        
        f.savefig(os.path.join(os.getcwd(),('DatasetTest\\Img'+ str(i) +'.jpg')))
    if Verbose == 2:
      for n in range(len(CTList)):
          
        N=n
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
      
        ax1.imshow(X[N,:,:,:])
    
        ax2.imshow(Xct[N,:,:])
        ax2.set_title('CT')
        
        ax3.plot(XDVH[1],Listy[0][N,:])
        ax3.set_title('Recto DVH')
        
        
        
        ax4.plot(XDVH[1],Listy[1][N,:])
        ax4.set_title('Vejiga DVH')
        f.savefig(os.path.join(os.getcwd(),('DatasetTest\\Img'+ str(n) +'.jpg')))

        plt.show()        