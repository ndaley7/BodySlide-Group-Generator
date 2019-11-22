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
from BSGG.__main__ import g_DebugEnabled

import os
import glob

from shutil import copy2 #So metadata is copied as well

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
    #Ensure Filename parity between sliderSetPath folder and the backup
    originalListXML=GetFileList(sliderPath,"*.xml")
    originalListOSP=GetFileList(sliderPath,"*.osp")

    #Concatenate both .OSP and .XML filelist for compatibility
    originalListXML.extend(originalListOSP)
    originalList=originalListXML
    #Check for existance of BackupBSCG Folder
    backupBSCGFound=os.path.isdir(sliderPath+"/BackupBSCG")

    #If Doesnt exist, create and copy all files from sliderSetPath Folder
    if(backupBSCGFound==True):
        #Ensure Filename parity between sliderSetPath folder and the backup
        backupListXML=GetFileList(sliderPath+"/BackupBSCG","*.xml")
        backupListOSP=GetFileList(sliderPath+"/BackupBSCG","*.osp")

        #Concatenate both .OSP and .XML filelist for compatibility
        backupListXML.extend(backupListOSP)
        backupList=backupListXML
        #Find difference between Backup and Original Lists
        difflist=list(set(originalList)-set(backupList))

        #Copy the missing files
        for file in difflist:
            copy2(file,sliderPath+"/BackupBSCG/"+os.path.basename(file))

        print("")
        print("")
        print("Backup Updated")
        print("")
        print("")

        #DEBUG

    elif(backupBSCGFound==False):
        #Create Backup folder
        os.makedirs(sliderPath+"/BackupBSCG")

        #Copy all files to backup
        for file in originalList:
            copy2(file,sliderPath+"/BackupBSCG/"+os.path.basename(file))

        print("")
        print("")
        print("Backup Created")
        print("")
        print("")


    
   
    
