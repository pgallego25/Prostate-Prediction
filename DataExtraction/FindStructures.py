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
    LFemoralListt=['Cap femur esq','FEMURESQ','femurE','OR-FE','Cap femur E','Cap femur esquerre','capfemoralesq','Cap Femur E','Cap fem Esq','cap femoral esq','cap femoral Esq','C. femoral E','cap femoral esquerre','femur esq']
    RFemoralListt=['Cap femur dret','FEMURDRTE','femurD','OR-FD','Cap femur D','Cap femu dret','capfemodret','Cap Femur D','cap fem dret','FEMURD','cap femoral dret','cap femoral D','C. femoral D','cap femur dret','femur dret','fèmur dret']
    PTV1List=['PTV1','PTV-P','P T V 1','p t v 1']
    PTV11List=['PTV11','PTV1 1','PTV1.1','PTV 11','PTV11 sib']

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
    
    
    
    
    
def FindStructuresBreast(RsPath,Side):
   
    if Side =='L':
        PulmonLList=['OR PULMO ESQ','OR-PULMOE','pulmon','PULMO ESQ OK','OR_PULMOE2','PULMO ESQ']
        PTVMamaList=['PTV MAMA ESQ','PTV PAREDI','PTV-MAMAI','PTV-MAMAE','PTV PARET ESQ','PTV pared','PTV-MAME','PTV paredMAMAESQ','PTV-PAREDI','PTV-MAMAE2','PTV-PARETESQ','PTV-MAMAESQ','PTV PARET']
    elif Side =='R':
        PulmonLList=['OR PULMO Dret','OR-PULMOD','OR PULMO DRET','OR-PULMON DRET','OR PULMO D','OR-PULMO DT','OR.PULMO DRET','OR-PDerecho','OR PULMO DRET2','pulmon','PULMO DRET']
        PTVMamaList=['PTV MAMA','PTV pared','PTV MAMA DRETA','PTV MAMA dreta','PTV-MAMAD','PTV pared derech','PTV PARET DRETA','PTV-PARETD','PTV PAREDD','PTV PARET D','PTV pared mamaD','PTV-PARETETD','PTV MAMA DRETA2','PTV-PAREDD','PTV MAMAD']

    CorList=['OR COR','OR-COR','Heart','corazon','OR_COR2']
    
    PTVAreaList=['PTV AREES','PTV AREAS','PTV-AREES','PTVareas','PTV-AREAS','PTV areas','PTV AREES D','PTV axilo-SC Dr','PTVAREES2CORREGI','PTV-APEX','PTV-AREE2','PTV AREASD','PTV- AREAS','PTV AREx']

    string = "Locations : "
    f = dicom.read_file(RsPath,force=True)
    for i in range(len(f.RTROIObservationsSequence)):
        string = string + " " +f.StructureSetROISequence[i].ROIName + "\n"
        if f.RTROIObservationsSequence[i].RTROIInterpretedType == 'EXTERNAL' :
            Body = i
            
        elif f.StructureSetROISequence[i].ROIName in PulmonLList:
    
            Pulmon =i
            
            
        elif f.StructureSetROISequence[i].ROIName in CorList:
    
            Cor =i
            
        
                  
        elif f.StructureSetROISequence[i].ROIName in PTVMamaList:
    
            PTVMama =i
        elif f.StructureSetROISequence[i].ROIName in PTVAreaList:
    
            PTVAreas =i
    
    print(string )      
    if Side == "L":
        return [Body,Pulmon,Cor,PTVMama,PTVAreas]
    else:
        return [Body,Pulmon,PTVMama,PTVAreas]
    