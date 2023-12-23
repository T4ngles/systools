"""

    Focus Reader
    Tool to remove unnecessary words to read faster.

    [ ] GUI
    [ ] Exe for windows or Kotlin implementation
    [ ] better error handling for text input
    [ ] input for text
    [ ] allow for paragraphs
    [ ] Extend functionality to website digests
    [ ] Scrape common words and add and maintain file of.
    [ ] forward analysis of common words

"""

import time
import sys
import re

#DEBUGGING

debugText = "Previously, you learned how organizations use security frameworks and controls to protect against threats, risks, and vulnerabilities. This included discussions about the National Institute of Standards and Technology’s (NIST’s) Risk Management Framework (RMF) and Cybersecurity Framework (CSF), as well as the confidentiality, integrity, and availability (CIA) triad. In this reading, you will further explore security frameworks and controls and how they are used together to help mitigate organizational risk."

#VARIABLES
COMMON_WORDS = ""#"a you how use and to this about the of as well in will they are".split(" ")

ERASE_LINE = '\x1b[2K'
CURSOR_UP_ONE = '\x1b[1A'

sleepTime = 0.12

debug = False

STREAM_READING = True


#FUNCTIONS
def splitWords(textInputStr: str):
    assert isinstance(textInputStr, str)
    
    #return textInputStr.split(" ")
    return re.split(" |\n", textInputStr)

def removeCommon(textInputList: list, commonWords: list):
    assert isinstance(textInputList, list)
    
    for word in COMMON_WORDS:
        while word in textInputList:
            textInputList.remove(word)

    return textInputList

def printDigest(digestWords: list):
    totalWords = len(digestWords)
    maxLengthWord = max(digestWords, key=len)
    maxLengthWordCharacters = len(maxLengthWord)
    padding = maxLengthWordCharacters//2

    
    for i, word in enumerate(digestWords):
        wordLength = len(word)
        wordPadding = (padding-wordLength//2)*" "
        trailer = (maxLengthWordCharacters-len(wordPadding)-wordLength)*" "

        if STREAM_READING:        
            if i > 0 and i < totalWords-1:
                print(f"{round(i/totalWords*100,0):.0f}% " + digestWords[i-1] +" "+ digestWords[i] +" "+ digestWords[i+1] +wordPadding, end="\r")
        else:
            print(f"{round(i/totalWords*100,0):.0f}% " + wordPadding + word + trailer, end="\r")
            
        time.sleep(sleepTime+0.01*wordLength)
        #sys.stdout.write(CURSOR_UP_ONE)
        #sys.stdout.write(ERASE_LINE)

#MAIN FUNCTION
if __name__ == '__main__':

    if debug:
        textInput = debugText
    else:
        print("Following common words will be removed.")
        print(COMMON_WORDS)
        print("Please provide text to summarise, press ctrl+c when done")
        textInput = ""
        while True:
            try:
                line = input()
            except KeyboardInterrupt:
                print("\n"*30)
                break
            textInput = textInput + "\n" + line
    
    textInputList = splitWords(textInput)

    digestWords = removeCommon(textInputList,COMMON_WORDS)

    printDigest(digestWords)
    
