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

import csv 
import requests 
import xml.etree.ElementTree as ET

def loadRSS(): 
  
    # url of rss feed 
    url = 'http://www.hindustantimes.com/rss/topnews/rssfeed.xml'
  
    # creating HTTP response object from given url 
    resp = requests.get(url) 
  
    # saving the xml file 
    with open('topnewsfeed.xml', 'wb') as f: 
        f.write(resp.content) 
          
  
def parseXML(xmlfile): 
  
    # create element tree object 
    tree = ET.parse(xmlfile) 
  
    # get root element 
    root = tree.getroot() 
  
    # create empty list for news items 
    newsitems = [] 
  
    # iterate news items 
    for item in root.findall('./channel/item'): 
  
        # empty news dictionary 
        news = {} 
  
        # iterate child elements of item 
        for child in item: 
  
            # special checking for namespace object content:media 
            if child.tag == '{http://search.yahoo.com/mrss/}content': 
                news['media'] = child.attrib['url'] 
            else: 
                news[child.tag] = child.text.encode('utf8') 
  
        # append news dictionary to news items list 
        newsitems.append(news) 
      
    # return news items list 
    return newsitems 
  
  
def savetoCSV(newsitems, filename): 
  
    # specifying the fields for csv file 
    fields = ['guid', 'title', 'pubDate', 'description', 'link', 'media'] 
  
    # writing to csv file 
    with open(filename, 'w') as csvfile: 
  
        # creating a csv dict writer object 
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
  
        # writing headers (field names) 
        writer.writeheader() 
  
        # writing data rows 
        writer.writerows(newsitems) 
  
      
def main(): 
    # Load Config File
    configXML=parseXML('Config.xml')
    
    #Store SliderGroups and SliderSet Paths
  
    #Generate list of Already Grouped Outfits
    
    #Generate new SliderGroup files for thos in the Unassigned BS Category

    #Writeout Status to console (Orignial Group # Final Group # Full Group List)
      
      
if __name__ == "__main__": 
  
    # calling main function 
    main() 