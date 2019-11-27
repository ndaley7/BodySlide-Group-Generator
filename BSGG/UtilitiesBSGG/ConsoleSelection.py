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




#Accpets a (Group, OutfitCount) tuple to be assigned a supergroup
#Outputs a (Supergrout,Subgroup,outfitCount) Tuple List With the finalzied group Conversions
def ConsoleSelectHelper(inputGroup,manualSelectBool):
    #init
    OutputGroupConvertions=[]
    subgroupList=[i[0] for i in inputGroup]
    superGroupName=str(inputGroup[0][0])
    inputIdx=0
    outfitTotal=0
    selectOption='0'
    splitIdxValid=False
    inputGroupLength=len(inputGroup)
    defaultInputGroupName=inputGroup[0][0]
    #Console Argument Count
    argc=0

    
    

    while (selectOption!=str(1) and selectOption!=str(2) and selectOption!=str(3)):#Loop until only one argument is input
        

        if(manualSelectBool==True):
            #Start Text Out
            #Writeout Group Layout
            print("Custom Group "+inputGroup[0][0]+" contains SubGroups :")
    
            #List out subgroups and outfits in format: "GroupName-> #Outfits"
            while inputIdx<len(inputGroup):
                print("( "+str(inputIdx)+" )-> "+ str(inputGroup[inputIdx][0]) +" with "+ str(inputGroup[inputIdx][1]) +" Outfits")

                #Add to total Outfit count
                outfitTotal=outfitTotal+inputGroup[inputIdx][1]
                inputIdx=inputIdx+1

            #Spacing to Leave a gap in terminal
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            #Total Outfit Printout    
            print(" Total of "+ str(outfitTotal) +" Outfits")
            print(" ")
            print(" ")
            print("Would you like to:")
            print(" ")
            print("( 1 ): Keep SuperGroup As Is")
            print("( 2 ): Rename This SuperGroup")
            print("( 3 ): Split SuperGroup (Coming in Version 1.3)")

            choices = input('-->: ')
            selected = [x for x in choices.split()]

        else:
            selected=[1,2,3]

       #Implement the selected Choice
        #implementing fix for if nothing has been input into the console
        argc=len(selected)

        if (argc>0):
            #If the argument count isnt greater than zero then ignore the input and loop again
            selectOption = str(selected[0])

        
        
        if(selectOption==str(1)):#Keep
            print("Assigning SubGroups")

            #Reassign all subgroup names to match the supergroup:
            for groupTuple in inputGroup:
                conversionTuple=(superGroupName,groupTuple[0],groupTuple[1])
                OutputGroupConvertions.append(conversionTuple)



        elif(selectOption==str(2)):#Rename
            print("Renaming")
            nameAlternate = str(input('Type Alternate name: '))
            #CHECK THIS:  Does it fix weird character entry in the console
            selectedName=''.join(e for e in nameAlternate if e.isalnum())

            #Reassign all subgroup names to match the supergroup:
            for groupTuple in inputGroup:
                conversionTuple=(selectedName.capitalize(),groupTuple[0],groupTuple[1])
                OutputGroupConvertions.append(conversionTuple)

        elif(selectOption==str(3)): #Split into multiple supergroups
            print("Option3")
            print("Split Selected")
            outfitTotal=0
            #Loop the split process until there are no more entries in the inputGroup list.
            while(len(inputGroup)>0):
                #Request the Split Index (Inclusive)
                while (splitIdxValid==False):

                    splitchoices = input('Select Beginning and ending indices (inclusive): ')
                    #Check to make sure two IDs were enetered
                    if (len(splitchoices.split())==2):
                        splitIdxs= [x for x in splitchoices.split()]
                        splitStart= int(splitIdxs[0])
                        splitEnd=int(splitIdxs[1])

                        #Check to ensure id selections are valid
                        if( splitStart>splitEnd or splitEnd>(inputGroupLength-1)):
                            splitIdxValid=False
                            print('Make sure that StartID < EndID <= Length of Selection List')
                        else:
                            splitIdxValid=True
                    else:
                        splitIdxValid=False
                        print('Make sure Indices follow the format ""StartID EndID"" ')
                #Sublist the selected indices and remove members from inputGroup
                splitList=inputGroup[splitStart:splitEnd+1]
                #Check and ensure this delete is working
                for i in sorted(range(splitStart,splitEnd+1), reverse=True):
                    del inputGroup[i]
                #Indexes selected, dislpay split group
                print("Split Selection Contains : ")
                #List out subgroups and outfits in format: "GroupName-> #Outfits"
                splitIdx=0
                while splitIdx<len(splitList):
                    print("( "+str(splitIdx)+" )-> "+ str(splitList[splitIdx][0]) +" with "+ str(splitList[splitIdx][1]) +" Outfits")

                    #Add to total Outfit count
                    outfitTotal=outfitTotal+splitList[splitIdx][1]
                    splitIdx=splitIdx+1
                print(" Total of "+ str(outfitTotal) +" Outfits")
                
                #Enter a name for this group or press Enter for name 'DEFAULTNAME'
                print('Enter a name for this selection or press Enter for default')
                splitNameInput = input('-->: ')

                #Check for Default
                if(splitNameInput==''):
                    #Name is empty, do default Naming
                    selectedSplitName=defaultInputGroupName
                else:
                    print('Setting name of selected groups to '+ str(splitNameInput))
                    selectedSplitName=splitNameInput

                for splitGroup in splitList:
                    conversionTuple=(selectedSplitName.capitalize(),splitGroup[0],splitGroup[1])
                    OutputGroupConvertions.append(conversionTuple)
                #Reset for remainder of Group Entries
                outfitTotal=0
                splitIdx=0
                #Display remaining inputGroup Entries and see if another subselection wants to be made.
                if(len(inputGroup)>0):
                    print('There are '+str(len(inputGroup))+' Groups Remaining')
                    print("Would you like to:")
                    print(" ")
                    print("( 1 ): Group Under Default Name: "+ defaultInputGroupName)
                    print("( 2 ): Group Under Custom Name")
                    print("( 3 ): Split Groups")
                    print('')
                    choices2 = input('-->: ')
                    #Check Input Length for Null input
                    argc2=len(choices2)
                    if (argc2>0):
                        selected2 = [x for x in choices2.split()]
                        
                        selectOption2 = str(selected2[0])
                        #Check selectOption2 for action
                        if(selectOption2==str(1)):#Keep
                            print("Assigning SubGroups")

                            #Reassign all subgroup names to match the supergroup:
                            for groupTuple in inputGroup:
                                conversionTuple=(defaultInputGroupName,groupTuple[0],groupTuple[1])
                                OutputGroupConvertions.append(conversionTuple)



                        elif(selectOption2==str(2)):#Rename
                            print("Renaming")
                            nameAlternate = str(input('Alternate Name ->>: '))
                            #CHECK THIS:  Does it fix weird character entry in the console
                            selectedName=''.join(e for e in nameAlternate if e.isalnum())

                            #Reassign all subgroup names to match the supergroup:
                            for groupTuple in inputGroup:
                                conversionTuple=(selectedName.capitalize(),groupTuple[0],groupTuple[1])
                                OutputGroupConvertions.append(conversionTuple)

                        elif(selectOption2==str(3)):#Split Loop again
                            print('Split:')
                            #Reset Control Variables
                            splitIdxValid=False
                            #List out subgroups and outfits in format: "GroupName-> #Outfits"
                            inputIdx=0
                            while inputIdx<len(inputGroup):
                                print("( "+str(inputIdx)+" )-> "+ str(inputGroup[inputIdx][0]) +" with "+ str(inputGroup[inputIdx][1]) +" Outfits")
                                

                                #Add to total Outfit count
                                outfitTotal=outfitTotal+inputGroup[inputIdx][1]
                                inputIdx=inputIdx+1


                    else:
                        print('Strange input detected, Using default name for remainder')
                        #Name the remainder of the Input Group entries after the default
                        for groupTuple in inputGroup:
                            conversionTuple=(defaultInputGroupName.capitalize(),groupTuple[0],groupTuple[1])
                            OutputGroupConvertions.append(conversionTuple)
                else:
                    print('All Groups Named')

                
                
            
            
            
            
        else:
            print(" ")
            print("--------Improper Input Detected--------------")
        

            
            if(argc>1):
                print("--------Please Select only one Option--------")
                print(" ")

        

                    
    return OutputGroupConvertions

