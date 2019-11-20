

#Accpets a (Group, OutfitCount) tuple to be assigned a supergroup
#Outputs a (Supergrout,Subgroup,outfitCount) Tuple List With the finalzied group Conversions
def ConsoleSelectHelper(inputGroup):
    #init
    OutputGroupConvertions=[]
    subgroupList=[i[0] for i in inputGroup]
    superGroupName=str(inputGroup[0][0])
    inputIdx=0
    outfitTotal=0
    selectOption='0'
    #Console Argument Count
    argc=0

    

    while (selectOption!=str(1) and selectOption!=str(2) and selectOption!=str(3)):#Loop until only one argument is input
        
        #Start Text Out
        #Writeout Group Layout
        print("SuperGroup "+inputGroup[0][0]+" contains SubGroups :")
    
        #List out subgroups and outfits in format: "GroupName-> #Outfits"
        while inputIdx<len(inputGroup):
            print("( "+str(inputIdx)+" )-> "+ str(inputGroup[inputIdx][0]) +" with "+ str(inputGroup[inputIdx][1]) +" Outfits")

            #Add to total Outfit count
            outfitTotal=outfitTotal+inputGroup[inputIdx][1]
            inputIdx=inputIdx+1

        #Total Outfit Printout    
        print(" Total of "+ str(outfitTotal) +" Outfits")
        print(" ")
        print(" ")
        print("Would you like to:")
        print(" ")
        print("( 1 ): Keep SuperGroup As Is")
        print("( 2 ): Rename This SuperGroup")
        print("( 3 ): Split SuperGroup")

        choices = input('Selected Option: ')
        selected = [x for x in choices.split()]

        

       #Implement the selected Choice

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
                conversionTuple=(selectedName,groupTuple[0],groupTuple[1])
                OutputGroupConvertions.append(conversionTuple)

        elif(selectOption==str(3)): #Split into multiple supergroups
            print("Option3")
            print("Split Functionality Currently in progress")
        else:
            print(" ")
            print("--------Improper Input Detected--------------")
        

            argc=len(selected)
            if(argc>1):
                print("--------Please Select only one Option--------")
                print(" ")

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

                    
    return OutputGroupConvertions

