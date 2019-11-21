
#import lxml
import lxml.etree as ET



def CreateConfigBSGGXML(bodyslideFilepath,debugLogStatus):
    #Intiate Root
    rootConfigXML=ET.Element('SliderGroupGeneratorConfig')

    #Add in Subfolder Paths

    ET.SubElement(rootConfigXML,'SliderGroupsPath').text=bodyslideFilepath+str("/SliderGroups")
    ET.SubElement(rootConfigXML,'SliderSetsPath').text=bodyslideFilepath+str("/SliderSets")
    ET.SubElement(rootConfigXML,'SliderCategoriesPath').text=bodyslideFilepath+str("/SliderCategories")
    ET.SubElement(rootConfigXML,'SliderPresetsPath').text=bodyslideFilepath+str("/SliderPresets")

    #Add in DebugStatus
    ET.Comment('Enable the below option for Verbose Debugging Log')
    ET.SubElement(rootConfigXML,'EnableDebugBSGG').text=str(debugLogStatus)
    
    #Write out the XML file
    my_tree = ET.ElementTree(rootConfigXML)
    with open('ConfigBSGG.xml','wb') as f: ## Write document to file
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
    # Test for path Existance and write out if good:

    # return news items list 
    return bsPaths