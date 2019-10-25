"""
NIND's BodySlide Utilites
by NIND

Created to work with BodySlide 2 and Outfit Studio
by Caliente

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
#Import of Modules used
import os
import ntpath
import glob
import csv 
import requests
 
import xml.etree.ElementTree as ET

#Global Variables

g_bodyslideGroupedOutfitsOnly=set() #Non Repeating Set (Python) of all grouped outfits
g_bodyslideGroupedOutfitsWGroup=set()#Set (Python) of Tuples (Python) Containing all Groups and Member outfits


def LoadConfigXML(configFile): 
    # Variables
    bsPaths = []
    # create element tree object 
    tree = ET.parse(configFile) 
  
    # get root element 
    root = tree.getroot() 
   
    #Append the two paths to the output array
    
    bsPaths.append(root[0].text)
    bsPaths.append(root[1].text)  
    # Test for path Existance and write out if good:

    # return news items list 
    return bsPaths

def ParseSliderGroupXML(fileWithPath):
    #This fxn will accept a SliderGroups .xml file and add the contents to a running outfit list and a Master Grouping XML file
    #Variables
    fileListing=[]

    #Load in XML Tree 
    tree = ET.parse(fileWithPath) 
    root = tree.getroot()

    #Parse through every <Group> tag
    for group in root.findall('Group'):
        #g_bodyslideGroupedOutfitsOnly.add(group.name)
        #Parse every <Member> tag
        groupName=group.get('name')

        for member in group.findall('Member'):
            #Add Group and Member to a Tuple (Python) containing both values
            memberName=member.get('name')
            outfitGroupMember=(groupName,memberName)
            g_bodyslideGroupedOutfitsWGroup.add(outfitGroupMember)

            #Check if Member Outfit is already in the MasterList
            if member.get('name') in g_bodyslideGroupedOutfitsOnly:
                print("Already Added to Master: "+member.get('name'))
            else:
                g_bodyslideGroupedOutfitsOnly.add(member.get('name'))

#This function accepts a full Path .xml SliderSet File.  It checks against the Master Outfit Grouping list.
#If the Outfits within the file are not grouped, they will be added to the master list and assigned a group named:
#"XML FILENAME" + "SLIDERSET NAME"
def ParseSliderSetXML(fileWithPath):
    #This fxn will accept a SliderSet .xml file and compare the contents to the outfit Masterlist
    #Variables
    fileListing=[]

    #Load in XML Tree 
    tree = ET.parse(fileWithPath) 
    root = tree.getroot()

    #Parse through every <Group> tag
    for group in root.findall('Group'):
        #g_bodyslideGroupedOutfitsOnly.add(group.name)
        #Parse every <Member> tag
        groupName=group.get('name')

        for member in group.findall('Member'):
            #Add Group and Member to a Tuple (Python) containing both values
            memberName=member.get('name')
            outfitGroupMember=(groupName,memberName)
            g_bodyslideGroupedOutfitsWGroup.add(outfitGroupMember)

            #Check if Member Outfit is already in the MasterList
            if member.get('name') in g_bodyslideGroupedOutfitsOnly:
                print("Already Added to Master: "+member.get('name'))
            else:
                g_bodyslideGroupedOutfitsOnly.add(member.get('name'))
        

    
   
    #Return the File List (With Full Path)   
    return fileListing

#This function accepts a full Path .osp SliderSet File.  It checks against the Master Outfit Grouping list.
#If the Outfits within the file are not grouped, they will be added to the master list and assigned a group named:
#"OSP FILENAME" + "SLIDERSET NAME"
def ParseSliderSetOSP(fileWithPath):
    #This fxn will accept a SliderSet .osp file and compare the contents to the outfit Masterlist
    #Variables
    fileListing=[]

    #Load in XML Tree 
    tree = ET.parse(fileWithPath) 
    root = tree.getroot()

    #Assign Potential Group Name
    
    #Parse through every <SliderSet> tag
    for sliderSet in root.findall('SliderSet'):
        
        #Check if SliderSet Outfit is already in the MasterList
        if sliderSet.get('name') in g_bodyslideGroupedOutfitsOnly:
            print("SliderSet Present in Master: "+member.get('name'))
        else:
            outfitGroupMember=(groupName,memberName)
            g_bodyslideGroupedOutfitsWGroup.add(outfitGroupMember)
            g_bodyslideGroupedOutfitsOnly.add(member.get('name'))
           

    #Return the File List (With Full Path)   
    return fileListing

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

def CatalogGroupedOutfits(sliderGroupPath):
    #This function generates the list of XML files in the SliderGroup Folder and passes them to be Parsed
    #Variables
    fileListing=[]
    #Get list of all files in the group folder (.xml)
    fileListing=GetFileList(sliderGroupPath,"*.xml")
    #Parse through each file Adding Groups and Outfits to overall collection
    for groupXML in fileListing: 
      ParseSliderGroupXML(groupXML)  
    return True

def CheckSliderSetOSP(sliderSetPath): 
    #Variables
    fileListing=[]
    #Get list of all files in the group folder (.osp)
    fileListing=GetFileList(sliderSetPath,"*.osp")
    #Parse through each file Adding Groups and Outfits to overall collection
    for setOSP in fileListing: 
      ParseSliderSetOSP(setOSP)  
    return True

def CheckSliderSetXML(sliderSetPath): 
    #Variables
    fileListing=[]
    #Get list of all files in the group folder (.xml)
    fileListing=GetFileList(sliderSetPath,"*.xml")
    #Parse through each file Adding Groups and Outfits to overall collection
    for setXML in fileListing: 
      ParseSliderSetXML(setXML)  
    return True

     

  
      
def main():
    #Initialize Variables
    bodyslidePaths=[]
    sliderSetXMLPaths=[]
    sliderSetOSPPaths=[]
      
    #Load Config File
    bodyslidePaths=LoadConfigXML('Config.xml')

    #Store SliderGroups and SliderSet Paths
    sliderGroupPath=bodyslidePaths[0]
    sliderSetPath=bodyslidePaths[1]
    
    #Generate list of Already Grouped Outfits
    CatalogGroupedOutfits(sliderGroupPath)

    #Generate lists of paths to .xml and .osp files in the SliderSet Folder
    sliderSetXMLPaths=GetFileList(sliderSetPath,'*.xml')
    sliderSetOSPPaths=GetFileList(sliderSetPath,'*.osp')

    #Loop through lists of OSP and XML files and process them.
    #SliderSet XML Reader
    for setXML in sliderSetXMLPaths: 
      ParseSliderSetXML(setXML)

    #SliderSet OSP Reader
    for setOSP in sliderSetOSPPaths: 
      ParseSliderSetOSP(setOSP)


    #Writeout Status to console (Orignial Group # Final Group # Full Group List)
      
      
if __name__ == "__main__": 
  
    # calling main function 
    main() 

    #Errors to Try and Catch:
    #Wrong Set folder location (Check for detection of Set format xml/osp files)
    #Wrong Group folder location (Check for detection of Set format xml files)
    #Check for Presence of the above paths in config.xml, if not present, ask for them
    #Check for Presence of Masterlist


    #Planned Features:
    #Select CBBE/UNP/Agnostic Mode to allow for checking of outfits that dont conform to the bodytype used in a game.
    #Automatic Grouping of Ungrouped Outfits with reasonable names

    #Load and Consolodation of SliderGroups to one Group File
        #-Option to Comprise Masterlist of only nongrouped outfits
    
    #Automatically Copy specified preset across all existing outfits

