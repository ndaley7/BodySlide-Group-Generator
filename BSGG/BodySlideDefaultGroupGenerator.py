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
import sys
import ntpath
import glob
import csv 
import requests
#import lxml
import lxml.etree as ET
#import difflib
from difflib import SequenceMatcher
#Import Functions

#from .UtilitiesBSGG.FileListing import GetFileList
 

#parser = ET.XMLParser(encoding="utf-8")
#tree = ET.fromstring(xmlstring, parser=parser)

#Global Variables

g_bodyslideGroupedOutfitsOnly=set() #Non Repeating Set (Python) of all grouped outfits
g_bodyslideGroupedOutfitsWGroup=[] #List (Python) of Tuples (Python) Containing all Groups and Member outfits
g_bodyslideNewGroupedOutfitsWGroup=[]
g_xmlEncodingString="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"

g_utf8_parser = ET.XMLParser(encoding='utf-8')
g_unicode_parser = ET.XMLParser(encoding='cp1252',ns_clean=True, recover=True)
#Accepts an XML format file with full path and checks for the presence of the XML encoding at the beginning of the document.
#Assuming encoding: for windows 10
def XMLEncodingConfirm(checkFile):

    f = open(checkFile, 'r')
    line = f.readline()

    if g_xmlEncodingString in line:
        f.close()
    else:
        f.close()
        with open(checkFile, 'r', encoding="cp1252") as original: data = original.read()
        #with open(checkFile, 'w', encoding="cp1252") as modified: modified.write(g_xmlEncodingString+"\n" + data)
        with open(checkFile, 'w', encoding="utf-8") as modified: modified.write(data)

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

    f = open(checkFile,'w')
    f.write(newdata3b)
    f.close()

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

def LoadConfigXML(configFile): 
    # Variables
    bsPaths = []
    # create element tree object
    parser = ET.XMLParser(remove_comments=True)
    tree = ET.parse(configFile,parser=parser) 
    
  
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
            if member.get('name') in g_bodyslideGroupedOutfitsOnly:
                print("Already Added to Master: "+member.get('name'))
            else:
                g_bodyslideGroupedOutfitsOnly.add(member.get('name'))

#This function accepts a full Path .xml/osp SliderSet File.  It checks against the Master Outfit Grouping list.
#If the Outfits within the file are not grouped, they will be added to the master list and assigned a group named:
#"SLIDERSET FILENAME" + "SLIDERSET NAME"
def ParseSliderSet(fileWithPath,fileName):
     #This fxn will accept a SliderSet .xml/osp file and compare the contents to the outfit Masterlist
    #Variables
    fileListing=[]

    #Load in XML Tree 
    #tree = ET.parse(fileWithPath,g_unicode_parser)
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
        ParseSliderGroupXML(groupXML)  
    return True

def TupleList2SliderGroupXML(tupleListIn,sliderGroupPath):
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
    with open(sliderGroupPath+'MasterList.xml','wb') as f: ## Write document to file
        f.write(ET.tostring(my_tree,pretty_print=True))
        #f.write(ET.tostring(rootMasterXML,encoding='utf-8', xml_declaration=True,pretty_print=True))
        #ET.write(sliderGroupPath+'MasterList.xml', encoding='utf-8', xml_declaration=True, pretty_print=True) 


#This function will configure a ConfigBSGG.xml file by asking the user questions on the command line
#Afterwards it will save a 'ConfigBSGG.xml' file in the same directory  as the executeable.
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
    return bodyslideCustomGroups



#This function will take in a list of tuples of the format (Group,Outfit)
#Return a list of tuples format (Group,ContainedOutfitCount) With each Group occuring once.
def ListGroupsOutfitNumber(groupOutfitTupleList):
    #init Variables
    groupOutfitNumber=[]
    referenceGroup=groupOutfitTupleList[0][0]
    outfitCount=1

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
    #Initialize Variables
    bodyslidePaths=[]
    sliderSetXMLPaths=[]
    sliderSetOSPPaths=[]

    #Check for the existance of a Config.xml file
    configExists=os.path.exists('Config.xml')
    if configExists:
        print("Config.xml Detected")
    else:
        print("Config.xml Not Detected.  Running Configurator")
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
        XMLEncodingConfirm(setXML)
        fileWithExtension=os.path.basename(setXML)
        fileWithoutExtension=os.path.splitext(fileWithExtension)[0] 
        ParseSliderSet(setXML,fileWithoutExtension)

    #SliderSet OSP Reader
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

        #Sort Groupings into a single Occurence List Of Tuples (Groupname,Outfits)
        existingGroupsWithOutfitNumber=ListGroupsOutfitNumber(g_bodyslideNewGroupedOutfitsWGroup)
        #Give Use Choices over Custom Groupings
        customBodyslideGroupedOutfits=GroupingConcatenationByName(existingGroupsWithOutfitNumber)

    else:
        #Assign the Default grouping
        customBodyslideGroupedOutfits=g_bodyslideNewGroupedOutfitsWGroup
      
    #Ask if user wants to generate a master list with all existing groups

    #Check if a masterlist already exists

    #Writeout Masterlist

    TupleList2SliderGroupXML(customBodyslideGroupedOutfits,sliderGroupPath)
if __name__ == "__main__": 
  
    # calling main function 
    main() 

    #Errors to Try and Catch:
    #Check for the Presence of Config.xml and ask questions to create it if it doesnt exist.
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

