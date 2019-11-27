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

#Import of Modules used
import os
import sys
import ntpath
import glob
import csv 
import requests
#import lxml
import lxml.etree as ET
#import difflib
from difflib import SequenceMatcher

#Tk


#import django for encoding issues
from django.utils.encoding import smart_str
#Local Application Imports
from .ParsingBSGG.XMLIO import LoadConfigXML

from .UtilitiesBSGG.ConsoleSelection import ConsoleSelectHelper
from .UtilitiesBSGG.UITkSelection import BodySlidePathSelect
from .UtilitiesBSGG.UITkSelection import CustomYesNoTF
from .UtilitiesBSGG.FileIO import GetFileList
from .UtilitiesBSGG.FileIO import SliderSetBackup
from .UtilitiesBSGG.FileIO import MasterListCheck
from .UtilitiesBSGG.BSCGLogging import BSCGDebugInit
from .UtilitiesBSGG.BSCGLogging import LoggingInfoBSCG
from .UtilitiesBSGG import GlobalDebug 

#Debugging

GlobalDebug.g_DebugEnabled=False

 

#parser = ET.XMLParser(encoding="utf-8")
#tree = ET.fromstring(xmlstring, parser=parser)

#Global Variables



#Global Lists (Needs to be taken out of the Global Scope)
g_bodyslideGroupedOutfitsOnly=set() #Non Repeating Set (Python) of all grouped outfits
g_bodyslideGroupedOutfitsWGroup=[] #List (Python) of Tuples (Python) Containing all Groups and Member outfits
g_bodyslideNewGroupedOutfitsWGroup=[]
g_xmlEncodingString="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"

#lxml Parsers with various encodings
g_utf8_parser = ET.XMLParser(encoding='utf-8')
g_latin1_parser = ET.XMLParser(encoding='latin1')
g_unicode_parser = ET.XMLParser(encoding='cp1252')
#g_unicode_parser = ET.XMLParser(encoding='cp1252',ns_clean=True, recover=True)
#Accepts an XML format file with full path and checks for the presence of the XML encoding at the beginning of the document.
#Assuming encoding: for windows 10
def XMLEncodingConfirm(checkFile):

    f = open(checkFile, 'r')
    line = f.readline()

    if g_xmlEncodingString in line:
        f.close()
    else:
        f.close()
        with open(checkFile, 'r', encoding="latin-1") as original: data = original.read()
        modstring=smart_str(data,encoding='utf-8')
        with open(checkFile, 'w', encoding="utf-8") as modified: modified.write(modstring)

    #Check for the presence of double hyphens "--" in the comments:

    f = open(checkFile,'r')
    filedata = f.read()
    f.close()

    newdata1 = filedata.replace("<!--","<!xx")
    newdata1a = newdata1.replace("-->","xx>")
    newdata2 = newdata1a.replace("--","  ")
    newdata3 = newdata2.replace("xx>","-->")
    newdata3a = newdata3.replace("<!xx","<!--")
    newdata3b = newdata3a.replace("--->","-->")
    newdata4 = newdata3b.replace("&#x03","") #Incompatible XML string

    f = open(checkFile,'w')
    f.write(newdata4)
    f.close()


def ParseSliderGroupXML(fileWithPath,bodyslideGroupedOutfitsOnly):
    #This fxn will accept a SliderGroups .xml file and add the contents to a running outfit list and a Master Grouping XML file
    #Variables
    fileListing=[]

    #Load in XML Tree 
    #with open(fileWithPath, 'r') as xml_file:
        #tree = ET.fromstring(xml_file.read())
    #XMLEncodingConfirm(fileWithPath)
    parser = ET.XMLParser(remove_comments=True)
    tree = ET.parse(fileWithPath,parser=parser) 
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
            g_bodyslideGroupedOutfitsWGroup.append(outfitGroupMember)

            #Check if Member Outfit is already in the MasterList
            if member.get('name') in bodyslideGroupedOutfitsOnly:
                print("Already Added to Master: "+member.get('name'))
            else:
                bodyslideGroupedOutfitsOnly.add(member.get('name'))

#This function accepts a full Path .xml/osp SliderSet File.  It checks against the Master Outfit Grouping list.
#If the Outfits within the file are not grouped, they will be added to the master list and assigned a group named:
#"SLIDERSET FILENAME" + "SLIDERSET NAME"
def ParseSliderSet(fileWithPath,fileName):
     #This fxn will accept a SliderSet .xml/osp file and compare the contents to the outfit Masterlist
    #Variables
    fileListing=[]

    #Load in XML Tree 
    #tree = ET.parse(fileWithPath,g_unicode_parser)
    #tree = ET.parse(fileWithPath, parser=g_latin1_parser)  
    tree = ET.parse(fileWithPath, ET.XMLParser(ns_clean=True, recover=True))  
    #root = tree.getroot()
    root = tree.getroot()

    #Assign Potential Group Name
    #Extract the name of the current file it is in for the group
    groupName=fileName
    #Parse through every <SliderSet> tag
    #Use Xpath to parse for the Sliderset tag to deal with the ocassional <SliderSetInfo version="1"> Tag on some OSP files
    for sliderSet in root.findall('SliderSet'):
        
        #Check if SliderSet Outfit is already in the MasterList
        if sliderSet.get('name') in g_bodyslideGroupedOutfitsOnly:
            print("SliderSet Present in Master: "+sliderSet.get('name'))
        else:
            #If not present in the Master list, add along with Group

            memberName=sliderSet.get('name')
            print("Group "+groupName+" <- "+memberName)
            outfitGroupMember=(groupName,memberName)
            g_bodyslideNewGroupedOutfitsWGroup.append(outfitGroupMember)
            g_bodyslideGroupedOutfitsOnly.add(memberName)
           

    #Return the File List (With Full Path)   
    #return fileListing



def CatalogGroupedOutfits(sliderGroupPath):
    #This function generates the list of XML files in the SliderGroup Folder and passes them to be Parsed
    #Variables
    fileListing=[]
    #Get list of all files in the group folder (.xml)
    fileListing=GetFileList(sliderGroupPath,"*.xml")
    #Parse through each file Adding Groups and Outfits to overall collection
    for groupXML in fileListing:
        XMLEncodingConfirm(groupXML) 
        ParseSliderGroupXML(groupXML,g_bodyslideGroupedOutfitsOnly)  
    return True

def TupleList2SliderGroupXML(masterListXML,tupleListIn,sliderGroupPath):
    #Initiate Root of MasterList.xml
    rootMasterXML=ET.Element('SliderGroups')

    #Iterate through new outfit list

    for groupOutfitTuple in tupleListIn:
        #Assign Group and Outfit names to Local Variables
        groupName=groupOutfitTuple[0]
        outfitName=groupOutfitTuple[1]

        #Check to see if current Group has been added to SliderGroups
        groupNameMatch=rootMasterXML.findall(".//Group[@name=\""+groupName+"\"]")
        if not groupNameMatch:
            currGroup=ET.SubElement(rootMasterXML,'Group',{'name': groupName})
            print("Group Added:"+groupName)
            currGroup=rootMasterXML.find(".//Group[@name=\""+groupName+"\"]")
            ET.SubElement(currGroup,'Member',{'name': outfitName})
            print("<-Outfit: "+outfitName)        
                
        else:
            currGroup=rootMasterXML.find(".//Group[@name='"+groupName+"']")
            ET.SubElement(currGroup,'Member',{'name': outfitName})
            print("<-Outfit: "+outfitName)

    my_tree = ET.ElementTree(rootMasterXML)
    with open(sliderGroupPath+masterListXML,'wb') as f: ## Write document to file
        f.write(ET.tostring(my_tree,pretty_print=True))
        #f.write(ET.tostring(rootMasterXML,encoding='utf-8', xml_declaration=True,pretty_print=True))
        #ET.write(sliderGroupPath+'MasterList.xml', encoding='utf-8', xml_declaration=True, pretty_print=True) 


#This function will configure a ConfigBSCG.xml file by asking the user questions on the command line
#Afterwards it will save a 'ConfigBSCG.xml' file in the same directory  as the executeable.
def ConfigureConfigBSGGXML():
    #Ask for both SliderGroup and SliderSet folders
    sliderGroupInput=input("Please type in the path to SliderGroups Folder:")
    assert os.path.isdir(sliderGroupInput), "SliderGroups folder not detected at, "+str(sliderGroupInput)
    print("SliderGroup Folder Good!")

    sliderSetInput=input("Please type in the path to SliderSets Folder:")
    assert os.path.isdir(sliderSetInput), "SliderSets folder not detected at, "+str(sliderSetInput)
    print("SliderGroup Folder Good!")


#This Function will take in the List of Tuple (Group, Outfit) and provide addiitonal sorting options for the outfits
#For now, group selection will be implemented by through input on the command line
def GroupingConcatenationByName(tupleListIn):
    #Initializations
    bodyslideCustomGroups=[]
    runningMatchList=[]
    referenceString=tupleListIn[0][0]
    #Running Indeces
    tupleIdx=0
    startingIdx=0
    endingIdx=0
    groupIterator=0
    #String Compare
    matchedLengthOld=0

    #String Comparison Variables
    referenceString=tupleListIn[0][0]
    #Set String for comparison
    comparisonString=tupleListIn[1][0]

    #While loop terminating when i>length(tuplelist)
    while tupleIdx< len(tupleListIn):

        

        #Init SequenceMatcher
        SeqMatch=SequenceMatcher(None,comparisonString,referenceString)

        
        currGroupString=referenceString
        #Run Sequence Match and get the longest length
        matchedInfo=SeqMatch.find_longest_match(0,len(comparisonString),0,len(referenceString))
        matchedLength=matchedInfo[2]

        #Transition to single matching condition

        if(matchedLength<3 ):
            #groupIterator=groupIterator+1
            #endingIdx=tupleIdx-1
            
            
            #Create Tuple and append
            currCustomGroup=(currGroupString,startingIdx,endingIdx)

            runningMatchList.append(currCustomGroup)
            #currGroupString=(comparisonString[0:matchedLength]) 
        
            #Reassign Starting Index
            startingIdx=tupleIdx
            
            referenceString=comparisonString
            comparisonString=tupleListIn[tupleIdx][0]
            groupIterator=0

        
        #Assign Ending ID:
        endingIdx=tupleIdx
        #Iterate the counter
        tupleIdx=tupleIdx+1

        #Assign the new Comparison String
        if (tupleIdx != len(tupleListIn)):
            comparisonString=tupleListIn[tupleIdx][0]
        #This is the case for the finall item in the list to be read in.    
        else:
            #Create Tuple and append
            currCustomGroup=(currGroupString,startingIdx,len(tupleListIn)-1)

            runningMatchList.append(currCustomGroup)
    return runningMatchList



#This Function will accept both the SupergroupRange Tuple(SupergroupName,Start,End) and sorted UngroupedOutift Lis: (Group, Outfit) 
#Premade and an optional Custom group sort will be available for selection on the command line.
def CustomGroupSelection(superGroupsWithRange,globalUngroupedList,GroupOutfitNumberList):
    #Initializations
    groupOutfitFocus=[]
    customGroupOutfitList=[]
    #Running Indeces
    ungroupedIdx=0
    print("Initializing Group Selection:")

    #Option to Mass Auto-Group
    autoNameBool=CustomYesNoTF("Bodyslide Custom Grouper","Would you like to manually confirm each Custom Group?")

    #Loop going through the superGroup list
    for superGroup in superGroupsWithRange:
        groupOutfitFocus.clear()
        #CHECK THE NOTATION BELOW FOR CORRECT PERFORMANCE
        groupOutfitFocus=GroupOutfitNumberList[superGroup[1]:superGroup[2]+1]
        groupConverstionTupleList=ConsoleSelectHelper(groupOutfitFocus,autoNameBool)

        #Find total amount of Outfits
        subgroupList=[i[2] for i in groupConverstionTupleList]
        outfitTotal=sum(subgroupList)
        #Parse the globalUngroupedList and convert the groups specified.
         
        for conversionTuple in groupConverstionTupleList:
            #ungroupedIdx=0
            for conversionIdx in range(0,conversionTuple[2]):
                

                customNameOutfit=(conversionTuple[0],globalUngroupedList[ungroupedIdx][1])
                customGroupOutfitList.append(customNameOutfit)
                ungroupedIdx=ungroupedIdx+1

        #Add the selected groupings to the ouput Grouplist
        
        #customGroupOutfitList=globalUngroupedList

        
    return customGroupOutfitList



#This function will take in a list of tuples of the format (Group,Outfit)
#Return a list of tuples format (Group,ContainedOutfitCount) With each Group occuring once.
def ListGroupsOutfitNumber(groupOutfitTupleList):
    #init Variables
    groupOutfitNumber=[]
    referenceGroup=groupOutfitTupleList[0][0]
    outfitCount=0

    #Parse through the list of outfits and groups
    for GroupOutfit in groupOutfitTupleList:
        compareGroup=GroupOutfit[0]
        if (referenceGroup==compareGroup):
            outfitCount=outfitCount+1
        else:
            groupAndCount=(referenceGroup,outfitCount)
            groupOutfitNumber.append(groupAndCount)
            #Set the old reference to the compared group and reinitialize count
            referenceGroup=compareGroup
            outfitCount=1

    #Append the Final Group and Count
    groupAndCount=(referenceGroup,outfitCount)
    groupOutfitNumber.append(groupAndCount)

    return groupOutfitNumber

def main():
    print("BsCG x64 Startup.....")
    print("Checking for ConfigBSCG.xml.....")
    print("")
    #Initialize Variables
    bodyslidePaths=[]
    sliderSetXMLPaths=[]
    sliderSetOSPPaths=[]
    
    #Used for modifying the name of MasterList if previous ones exist
    masterListNum=0
    

    #Check for the existance of a ConfigBSCG.xml file
    configExists=os.path.exists('ConfigBSCG.xml')
    if configExists:
        print("ConfigBSCG.xml Detected")
        #LoggingInfoBSCG("ConfigBSCG.xml Detected")
    else:
        print("ConfigBSCG.xml Not Detected.  Running Configurator")
        #LoggingInfoBSCG("ConfigBSCG.xml Not Detected.  Running Configurator")
        BodySlidePathSelect()
    #Load Config File
    bodyslidePaths=LoadConfigXML('ConfigBSCG.xml')
    

    #Debug Init
    BSCGDebugInit()
    LoggingInfoBSCG("BSCG: Logging Session Start")
    #Store SliderGroups and SliderSet Paths (DEBUG done)
    sliderGroupPath=bodyslidePaths[0]
    sliderSetPath=bodyslidePaths[1]
    LoggingInfoBSCG("BSCG: SliderSet and SliderGroup Paths Found")
    #Run Backup Algorithm (DEBUG done)
    SliderSetBackup(sliderSetPath)
    SliderSetBackup(sliderGroupPath)

    #Check if a masterlist already exists and write out the naming modifier (DEBUG done)
    masterListNum=MasterListCheck(sliderGroupPath)
    
    #Generate list of Already Grouped Outfits (DEBUG X)
    CatalogGroupedOutfits(sliderGroupPath)

    #Generate lists of paths to .xml and .osp files in the SliderSet Folder(DEBUG X)
    sliderSetXMLPaths=GetFileList(sliderSetPath,'*.xml')
    sliderSetOSPPaths=GetFileList(sliderSetPath,'*.osp')

    #Loop through lists of OSP and XML files and process them.
    #SliderSet XML Reader(DEBUG X)
    for setXML in sliderSetXMLPaths:
        XMLEncodingConfirm(setXML)
        fileWithExtension=os.path.basename(setXML)
        fileWithoutExtension=os.path.splitext(fileWithExtension)[0] 
        ParseSliderSet(setXML,fileWithoutExtension)

    #SliderSet OSP Reader(DEBUG X)
    for setOSP in sliderSetOSPPaths:
        XMLEncodingConfirm(setOSP)
        fileWithExtension=os.path.basename(setOSP)
        fileWithoutExtension=os.path.splitext(fileWithExtension)[0]  
        ParseSliderSet(setOSP,fileWithoutExtension)

    #Sort List
    g_bodyslideNewGroupedOutfitsWGroup.sort()
    print("simple sort")
    #print(g_bodyslideNewGroupedOutfitsWGroup)
    #++Writeout Status to console (Orignial Group # Final Group # Full Group List)

    #See if User wants to modify Groupings
    modifyGroups=True

    if(modifyGroups):

        #Sort Groupings into a single Occurence List Of Tuples (Groupname,Outfits) (DEBUG X)
        existingGroupsWithOutfitNumber=ListGroupsOutfitNumber(g_bodyslideNewGroupedOutfitsWGroup)
        #Prep List for custom group selector (DEBUG X)
        presortedGroupsWithRange=GroupingConcatenationByName(existingGroupsWithOutfitNumber)
        #Console Outfit Group Selector (DEBUG X)
        customBodyslideGroupedOutfits=CustomGroupSelection(presortedGroupsWithRange, g_bodyslideNewGroupedOutfitsWGroup,existingGroupsWithOutfitNumber)
    else:
        #Assign the Default grouping (DEBUG X)
        customBodyslideGroupedOutfits=g_bodyslideNewGroupedOutfitsWGroup
      
    #Ask if user wants to generate a master list with all existing groups

    #Check if a masterlist already exists

    #Writeout Masterlist (DEBUG X)

    TupleList2SliderGroupXML('MasterList'+ str(masterListNum) +'.xml',customBodyslideGroupedOutfits,sliderGroupPath)


