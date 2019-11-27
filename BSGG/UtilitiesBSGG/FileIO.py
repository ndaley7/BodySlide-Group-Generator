"""
    This file is part of:
    NIND's BodySlide Utilites
    by NIND

    Created to work with BodySlide 2 and Outfit Studio
    by Ousnius

    This software is provided 'as-is', without any express or implied
    warranty. In no event will the authors be held liable for any
    damages arising from the use of this software.

    Permission is granted to anyone to use this software for any
    purpose, including commercial applications, and to alter it and
    redistribute it freely, subject to the following restrictions:

    1. The origin of this software must not be misrepresented; you must
    not claim that you wrote the original software. If you use this
    software in a product, an acknowledgment in the product documentation
    would be appreciated but is not required.

    2. Altered source versions must be plainly marked as such, and
    must not be misrepresented as being the original software.

    3. This notice may not be removed or altered from any source
    distribution.
"""


import os
import glob
import sys

from shutil import copy2 #So metadata is copied as well
#Local Imports
from .UITkSelection import CustomYesNoCancel
from .UITkSelection import CustomYesNoTF
from .UITkSelection import CustomWarning
from .UITkSelection import CustomError
from .BSCGLogging import LoggingInfoBSCG

#Returns a List of files within the specified filePath with specified fileExtension
def GetFileList(filePath,fileExtension):
    #Variables
    fileListing=[]

    #Get list of all files in the group folder (.fileExtension)
    os.chdir(filePath)
    for file in glob.glob(fileExtension):
        fileListing.append(filePath+file)
        print(file)
   
    #Return the File List (With Full Path)   
    return fileListing

#Checks for  BackupBSCG folder in the Sliderset folder
#Creates one if none exixsts and copies existing Sliderset Files
#If it does exist, ensures parity (Namewise) with the sliderset folder
def SliderSetBackup(sliderPath):
    #Variables
    LoggingInfoBSCG("BACKUP: Initializing Sliderset OSP/XML Backup")
    #Ensure Filename parity between sliderSetPath folder and the backup
    originalListXML=GetFileList(sliderPath,"*.xml")
    originalListOSP=GetFileList(sliderPath,"*.osp")

    #Concatenate both .OSP and .XML filelist for compatibility
    LoggingInfoBSCG("BACKUP: Concat XML and OSP files List")
    originalListXML.extend(originalListOSP)
    originalList=originalListXML
    #Check for existance of BackupBSCG Folder
    backupBSCGFound=os.path.isdir(sliderPath+"/BackupBSCG")

    #If Doesnt exist, create and copy all files from sliderSetPath Folder
    if(backupBSCGFound==True):
        #Ensure Filename parity between sliderSetPath folder and the backup
        backupListXML=GetFileList(sliderPath+"/BackupBSCG","*.xml")
        backupListOSP=GetFileList(sliderPath+"/BackupBSCG","*.osp")
        LoggingInfoBSCG("BACKUP: Folder Found")
        #Concatenate both .OSP and .XML filelist for compatibility
        backupListXML.extend(backupListOSP)
        backupList=backupListXML
        #Find difference between Backup and Original Lists
        difflist=list(set(originalList)-set(backupList))
        LoggingInfoBSCG("BACKUP:: "+str(len(difflist)) +" New Files")
        #Copy the missing files
        for file in difflist:
            copy2(file,sliderPath+"/BackupBSCG/"+os.path.basename(file))
            LoggingInfoBSCG("BACKUP: copied "+os.path.basename(file))

        print("")
        print("")
        print("Backup Updated")
        print("")
        print("")

        #DEBUG

    elif(backupBSCGFound==False):
        #Create Backup folder
        os.makedirs(sliderPath+"/BackupBSCG")
        LoggingInfoBSCG("BACKUP: Folder not found. Creating Folder")

        #Copy all files to backup
        for file in originalList:
            copy2(file,sliderPath+"/BackupBSCG/"+os.path.basename(file))
            LoggingInfoBSCG("BACKUP: copied "+os.path.basename(file))
        print("")
        print("")
        print("Backup Created")
        print("")
        print("")

#Checks for existing MasterListX.xml files
#Offers option to Delete existing ones or create another with a higher iterator
def MasterListCheck(sliderGroupPath):
    #Variables
    AvailableMasterList=False
    masterListIterator=0

    #List all MasterListX.xml files
    originalListXML=GetFileList(sliderGroupPath,"MasterList*.xml")

    if(len(originalListXML)==0):
        #DEBUG: No existing MasterLists detected
        LoggingInfoBSCG("CHECKMASTER: No Existing MasterListX.xml files found")
        masterListNumber=0
    elif(len(originalListXML)>0):
        #Ask YN for additional list creation
        mListAdditionalYN=CustomYesNoCancel("BodySlide Custom Grouper","MasterList(s) Detected. \n Make Additional List?")
        if(mListAdditionalYN==True):
            LoggingInfoBSCG("CHECKMASTER: mListAdditionalYN: Make additional MList")
            #Search for Available modifying number and make an additional list
            while(AvailableMasterList!=True):
                for masterList in originalListXML:
                    masterListName=os.path.basename(masterList)
                    masterListNameNew="MasterList"+str(masterListIterator)+".xml"

                    if(masterListName!=masterListNameNew):
                        AvailableMasterList=True
                        masterListNumber=masterListIterator

                masterListIterator=masterListIterator+1


        elif(mListAdditionalYN==False):
            #Remove all MasterList Files and create a new one?
            LoggingInfoBSCG("CHECKMASTER: mListAdditionalYN: No Additional MList Selected")
            mListDeleteYN=CustomYesNoTF("BodySlide Custom Grouper","Remove old MasterList files and Create Single File?")
            
            if(mListDeleteYN==True):
                #Delete all existing files with prefix 'MasterList' and create MasterList0.xml
                LoggingInfoBSCG("CHECKMASTER: mListDeleteYN: Delete existing MLists")
                masterListList=GetFileList(sliderGroupPath,"MasterList*.xml")
                CustomWarning("BodySlide Custom Grouper","About to delete "+str(len(masterListList))+" MasterList File(s). \n Rename them for safekeeping")
                for file in masterListList:
                    os.remove(file)
                masterListNumber=0
            else:
                LoggingInfoBSCG("CHECKMASTER: BSCG: SHUTDOWN")
                CustomWarning("BodySlide Custom Grouper","BSCG Shutting Down")
                exit()
        else:
            LoggingInfoBSCG("CHECKMASTER: BSCG: SHUTDOWN")
            CustomWarning("BodySlide Custom Grouper","BSCG Shutting Down")
            exit() #Terminate

        

    
    #Return the File List (With Full Path)   
    return masterListNumber
    
   
    
