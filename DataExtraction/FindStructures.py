# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 08:33:28 2018

@author: pgallego
"""
import pydicom as dicom
#Bladder, Rectum, Body Fermoales, PTV
RdPath = 'C:\\Users\\pgallego\\Desktop\\Prostate1\\RD.1.2.246.352.71.7.2101921327.432885.20121219084743.dcm'
RsPath = 'C:\\Users\\pgallego\\Desktop\\Prostate1\\RS.1.2.246.352.71.4.2101921327.18465.20121219102519.dcm'
# 


def FindStructures(RsPath):
    BufetaList=['Bufeta','bufeta','bllader','Bladder','BUFETA','BLADDER','bufet','VEJIGA','Vejiga']
    RectoList=['Recte','rectum','recte','recto','RECTO','RECTE','OR-RECTE','Recto']
    LFemoralListt=['Cap femur esq','FEMURESQ','femurE','OR-FE','Cap femur E','Cap femur esquerre','capfemoralesq','Cap Femur E','Cap fem Esq','cap femoral esq','cap femoral Esq','C. femoral E']
    RFemoralListt=['Cap femur dret','FEMURDRTE','femurD','OR-FD','Cap femur D','Cap femu dret','capfemodret','Cap Femur D','cap fem dret','FEMURD','cap femoral dret','cap femoral D','C. femoral D']
    PTV1List=['PTV1','PTV-P','P T V 1']
    PTV11List=['PTV11','PTV1 1','PTV1.1']

    string = "Locations : "
    f = dicom.read_file(RsPath,force=True)
    for i in range(len(f.RTROIObservationsSequence)):
        string = string + " " +f.StructureSetROISequence[i].ROIName
        if f.RTROIObservationsSequence[i].RTROIInterpretedType == 'EXTERNAL' :
            Body = i
            
        elif f.StructureSetROISequence[i].ROIName in BufetaList:
    
            Bufeta =i
            
            
        elif f.StructureSetROISequence[i].ROIName in RectoList:
    
            Recto =i
            
            
        elif f.StructureSetROISequence[i].ROIName in LFemoralListt:
    
            LFemoral =i
            
            
        elif f.StructureSetROISequence[i].ROIName in RFemoralListt:
    
            RFemoral =i
                  
        elif f.StructureSetROISequence[i].ROIName in PTV1List:
    
            PTV1 =i
        elif f.StructureSetROISequence[i].ROIName in PTV11List:
    
            PTV11 =i
    print(string)      
    return [Body,Recto,Bufeta,LFemoral,RFemoral,PTV1,PTV11]
    
    
    
    
    
