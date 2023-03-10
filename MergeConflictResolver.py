import glob


def mergeTwees(compiledTweeFileName):
    compiledLexia = []
    
    localTwees = glob.glob('./*.twee')
    
    print(f'\n--Twee Files Found - {len(localTwees)}: {localTwees}\n')
    
    for tweeFileName in localTwees:
        if tweeFileName == f".\{compiledTweeFileName}.twee":
            print(f"--Twee file to compile, {compiledTweeFileName}.twee, detected, overwriting...\n")
            localTwees.remove(tweeFileName)
            break
    
    for twee in localTwees:
        with open(twee) as tweeFile:
            content = tweeFile.read()
            lexiaList = content.split("::")
            
            if len(lexiaList) < 4:
                raise IndexError(f"{twee} does not have any content!")
            
            print(f"--Number of Passages in {twee}: {len(lexiaList) - 3}")     
            
            if localTwees.index(twee) == 0:
                compiledLexia += lexiaList[1:3]
            
            compiledLexia += lexiaList[3:]
            
            if localTwees.index(twee) != len(localTwees) - 1:
                compiledLexia[-1] += "\n\n"
    
    print()    
    lexiaNames = []
    for lexis in compiledLexia:
        nameWithLexisInfo = lexis.split("\n")
        nameWithLexisInfo = nameWithLexisInfo[0].strip()
        
        name = nameWithLexisInfo.split("{")
        name = name[0]
        name = name.strip()
        
        if name != "StoryTitle" and name != "StoryData":
            lexiaNames.append(name)
    
    duplicateLexia = [name for name in lexiaNames if lexiaNames.count(name) > 1]
    duplicateLexia = list(set(duplicateLexia))
    if len(duplicateLexia) > 0:
        print(f"--Duplicate Passages Found - {len(duplicateLexia)}: {duplicateLexia}\n")
        cullDuplicateLexia = input("Do you want to combine duplicate Passages (Y/N)? ")
        print()
        if cullDuplicateLexia[0].upper() == "Y":
            for duplicate in duplicateLexia:
                duplicateIndices = [i for i in range(len(lexiaNames)) if lexiaNames[i] == duplicate]
                lexiaToCombine = [compiledLexia[i + 2] for i in duplicateIndices]
                
                for lexis in lexiaToCombine:
                    compiledLexia.remove(lexis)
                
                combinedLexis = ""
                for lexis in lexiaToCombine:
                    splitLexis = lexis.split("}")
                    splitLexis[0] += "}"
                    
                    if lexiaToCombine.index(lexis) == 0:
                        combinedLexis += splitLexis[0]
                        
                    combinedLexis += "".join(splitLexis[1:])
                
                compiledLexia.append(combinedLexis)       
    
    compiledText = "::" + "::".join(compiledLexia)
    with open(f"{compiledTweeFileName}.twee", "w") as compiledTwee:
        compiledTwee.write(compiledText)
    
    print("v" * 90)
    print(f"Twee Files merged! Import {compiledTweeFileName}.twee into Twine 2.6+ to see the results!\n")


if __name__ == "__main__":
    print("Welcome to the Twine Commit Merger script, created by Randen Banuelos!")
    print("If you'd like to reference the guide, go to this URL: tinyurl.com/TwineCommitMergingGuide")
    print("v" * 90)
    compiledName = input("Please enter the name of the compiled .twee file to generate: ")
    print("v" * 90)
    mergeTwees(compiledName)
    _ = input("Press Enter to exit the Merger script...")