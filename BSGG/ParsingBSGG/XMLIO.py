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
#import lxml
import lxml.etree as ET
#import django for encoding issues
from django.utils.encoding import smart_str

from BSGG.UtilitiesBSGG import GlobalDebug
from BSGG.UtilitiesBSGG.BSCGLogging import LoggingInfoBSCG 

#Abbreviated Version of the disclaimer
g_xmlEncodingString="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
#lxml Parsers with various encodings
g_utf8_parser = ET.XMLParser(encoding='utf-8')
g_latin1_parser = ET.XMLParser(encoding='latin1')
g_unicode_parser = ET.XMLParser(encoding='cp1252')
#g_unicode_parser = ET.XMLParser(encoding='cp1252',ns_clean=True, recover=True)
liscenceAbbrev='placeholder'


def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False


#Accepts an XML format file with full path and checks for the presence of the XML encoding at the beginning of the document.
#Assuming encoding: for windows 10
def XMLEncodingConfirm(checkFile):

    f = open(checkFile, 'r')
    line = f.readline()

    if g_xmlEncodingString in line:
        LoggingInfoBSCG("XMLENCODE: UTF-8 xml header found") 
        f.close()
    else:
        f.close()
        LoggingInfoBSCG("XMLENCODE: latin-1 read attempt file: "+ os.path.basename(checkFile)) 
        with open(checkFile, 'r', encoding="latin-1") as original: data = original.read()
        modstring=smart_str(data,encoding='utf-8')
        LoggingInfoBSCG("XMLENCODE: utf-8 write attempt file: "+ os.path.basename(checkFile)) 
        with open(checkFile, 'w', encoding="utf-8") as modified: modified.write(modstring)

    #Check for the presence of double hyphens "--" in the comments:

    f = open(checkFile,'r')
    filedata = f.read()
    f.close()
    LoggingInfoBSCG("XMLENCODE: Removing (Bad Comments,Strange Characters)") 
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

def CreateConfigBSCGXML(bodyslideFilepath,debugLogStatus):
    #Intiate Root
    rootConfigXML=ET.Element('SliderGroupGeneratorConfig')
    pathComment = ET.Comment('File paths for the Bodyslide folders important to this tool. \n Note they all use / end with an occurence of /')

    rootConfigXML.append(pathComment)
    #Add in Subfolder Paths

    ET.SubElement(rootConfigXML,'SliderGroupsPath').text=bodyslideFilepath+str("/SliderGroups/")
    ET.SubElement(rootConfigXML,'SliderSetsPath').text=bodyslideFilepath+str("/SliderSets/")
    ET.SubElement(rootConfigXML,'SliderCategoriesPath').text=bodyslideFilepath+str("/SliderCategories/")
    ET.SubElement(rootConfigXML,'SliderPresetsPath').text=bodyslideFilepath+str("/SliderPresets/")

    finalpath=ET.Element('SliderPresetsPath')

    #Add in DebugStatus
    errorComment=ET.Comment('Enable the below option for Verbose Debugging Log (True/False)')
    finalpath.append(errorComment)
    ET.SubElement(rootConfigXML,'EnableDebugBSGG').text=str(debugLogStatus)
    
    #Write out the XML file
    my_tree = ET.ElementTree(rootConfigXML)
    with open('ConfigBSCG.xml','wb') as f: ## Write document to file
        f.write(ET.tostring(my_tree,pretty_print=True))

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
    GlobalDebug.g_DebugEnabled=str_to_bool(root[4].text)
    #LoggingInfoBSCG('ConfigBSCG.xml Variables found and parsed.')
    #Debug 
    # Test for path Existance and write out if good:

    # return news items list 
    return bsPaths