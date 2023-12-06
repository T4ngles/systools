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

#DEBUGGING

debugText = "Previously, you learned how organizations use security frameworks and controls to protect against threats, risks, and vulnerabilities. This included discussions about the National Institute of Standards and Technology’s (NIST’s) Risk Management Framework (RMF) and Cybersecurity Framework (CSF), as well as the confidentiality, integrity, and availability (CIA) triad. In this reading, you will further explore security frameworks and controls and how they are used together to help mitigate organizational risk."

#VARIABLES
COMMON_WORDS = "you how use and to this about the of as well in will they are".split(" ")

ERASE_LINE = '\x1b[2K'
CURSOR_UP_ONE = '\x1b[1A'

sleepTime = 0.3

debug = False

#FUNCTIONS
def splitWords(textInputStr: str):
    assert isinstance(textInputStr, str)
    
    return textInputStr.split(" ")
    

def removeCommon(textInputList: list, commonWords: list):
    assert isinstance(textInputList, list)
    
    for word in COMMON_WORDS:
        while word in textInputList:
            textInputList.remove(word)

    return textInputList

def printDigest(digestWords: list):
    
    for word in digestWords:
            print(word+100*" ", end="\r")
            time.sleep(sleepTime)
            #sys.stdout.write(CURSOR_UP_ONE)
            #sys.stdout.write(ERASE_LINE)

#MAIN FUNCTION
if __name__ == '__main__':

    if debug: textInput = debugText
    else: textInput = input("Please provide text to summarise:")
    
    textInputList = splitWords(textInput)

    digestWords = removeCommon(textInputList,COMMON_WORDS)

    printDigest(digestWords)
    
