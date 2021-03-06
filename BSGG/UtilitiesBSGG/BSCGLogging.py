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
#Enable Logging if Selected

import BSGG.UtilitiesBSGG.GlobalDebug
    

import logging
def BSCGDebugInit():
    
    if(BSGG.UtilitiesBSGG.GlobalDebug.g_DebugEnabled==True):
        logging.basicConfig(filename="logBSCG.txt",
                                    filemode='a',
                                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                    datefmt='%a, %d %b %Y %H:%M:%S',
                                    level=logging.DEBUG)
        logging.info("BSCG Session Logging Enabled")                            
    else:
        print("Logging Disabled")

def LoggingInfoBSCG(LogString):
    logging.info(LogString)
    

#self.logger = logging.getLogger('urbanGUI')