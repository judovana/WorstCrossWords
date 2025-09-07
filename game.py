import translate
import generateImage
import explain
import show_image
import caches
import generateWords

import threading
import random
from PIL import Image
import pathlib
import sys
import re

def getAllExplanationsFilesFor(word, lang):
    translatedId=caches.getTranslated(lang, word)
    explanationFilesTransalted=caches.getFilesFromTransaltedAiExplainCache(lang, translatedId)
    return explanationFilesTransalted

def getAllImageFilesFor(word, lang, ):
    translatedId=caches.getTranslated(lang, word)
    explanationImages=caches.getFilesFromAiImageCache(translatedId)
    return explanationImages

def createOrPlusPlus(dictItself, dictKey):
    if dictKey in dictItself:
        i=dictItself[dictKey]
        i=i+1
        dictItself[dictKey]=i
        return i;
    else:
        dictItself[dictKey]=0
        return 0

def processITGaz(cmd, desk, textIndexes, imagesIndexes,lang):
    cchar=cmd[1:][0].upper()
    idInt=generateWords.letterToId(cchar)
    ccmd=cmd[:1].upper()
    word=desk.wordsWithPlacement[idInt].word
    acro=''.join([cchar*len(word)])
    title=acro + " (" + str(len(word)) + ")";
    if ccmd == "T":
        index=createOrPlusPlus(textIndexes, cchar)
        allFiles=getAllExplanationsFilesFor(word, lang)
        if index >= len(allFiles):
            index=0
            textIndexes[cchar]=0
        print(title +" " + str(index+1)+"/"+str(len(allFiles)))
        print(pathlib.Path(allFiles[index]).read_text())
        return True
    if ccmd == "G":
        index=createOrPlusPlus(textIndexes, cchar)
        allFiles=getAllExplanationsFilesFor(word, lang)
        if index >= len(allFiles):
            index=0
            textIndexes[cchar]=0
        show_image.display_text(allFiles[index], title+" " + str(index+1)+"/"+str(len(allFiles)), 80)
        return True
    if ccmd == "I":
        index=createOrPlusPlus(imagesIndexes, cchar)
        allFiles=getAllImageFilesFor(word, lang)
        if index >= len(allFiles):
            index=0
            textIndexes[cchar]=0
        show_image.display_image(allFiles[index], title+" " + str(index+1)+"/"+str(len(allFiles)))
        return True

def processIITTGGaz(cmd, desk,lang):
    cchar=cmd[2:][0].upper()
    idInt=generateWords.letterToId(cchar)
    ccmd=cmd[:2].upper()
    word=desk.wordsWithPlacement[idInt].word
    acro=''.join([cchar*len(word)])
    title=acro + " (" + str(len(word)) + ")";
    if ccmd == "TT":
        for file in getAllExplanationsFilesFor(word, lang):
            print(title)
            print(pathlib.Path(file).read_text())
        return True
    if ccmd == "GG":
        for file in getAllExplanationsFilesFor(word, lang):
            show_image.display_text(file, title, 80)
        return True
    if ccmd == "II":
        for file in getAllImageFilesFor(word, lang):
            show_image.display_image(file, title)
        return True
   
def main():
    print("optional first argument is  argument file with all words. Optional second argument may follow - number of words.") 
    print("WARNING If no first first argument is given, weird `cs` lang is loaded") 
    print("WARNING the language is detected from file name. Be sure the only letters in the filename are identifying the lang as `cs` `en` or `de`") 
    print("Warning. environment vat "+caches.NOTRANS_VAR+"set to True, will skipp transaltion step.Note it may corrupt the caches, backup them before. Noe the AI being asked for different, then english words is weird")
    print("environment variable "+generateWords.SIZE_VAR+" in format WxH may be used to set size of  desk (be carefull)") 
    wordsFile="cs-20-2025-09-05_14:36:15"
    #wordsFile="cs"
    #wordsFile="de"
    #wordsFile="en"
    if len(sys.argv) > 1:
        wordsFile=sys.argv[1]
    wcount=5
    if len(sys.argv) > 2:
        wcount=int(sys.argv[2])
    lang= re.sub('[^a-z]+', '', wordsFile)
    print("lang is "+lang)
    caches.loadCache(lang)
    caches.doLog=False
    words=generateWords.readWorlist(wordsFile)
    random.shuffle(words)
    desk=generateWords.generate(words, wcount)
    for index, wwp in enumerate(desk.wordsWithPlacement):
        word=wwp.word
        #print(str(index)+"/"+str(len(desk.wordsWithPlacement))+" processing " + word)
        print(str(index)+"/"+str(len(desk.wordsWithPlacement))+" processing ")
        translatedId=caches.getTranslated(lang, word)
        explanationFilesTransalted=caches.getFilesFromTransaltedAiExplainCache(lang, translatedId)
        if not explanationFilesTransalted:
            caches.explainToCache(lang, translatedId)
        print("Found text/cached items: " + str(len(getAllExplanationsFilesFor(word, lang))))
        explanationImages=caches.getFilesFromAiImageCache(translatedId)
        if not explanationImages:
            caches.imageToCache(translatedId)
        print("Found image/cached items: " + str(len(getAllImageFilesFor(word, lang))))
    #cheat(desk)
    #desk.prettyPrint()
    print()
    desk.hideAll()
    desk.prettyPrint()
    qhelp="help exit L ? ?n ?? (? ?n ?? I In II T G Tn TT GG newI newT delIn delTn)[a-z] `sub[A-Z] guess`"
    history=[];
    comandsUsage = {}
    imagesIndexes={}
    textIndexes={}
    print(qhelp)
    for line in sys.stdin:
        print(qhelp)
        cmd=line.strip()
        history.append(cmd);
        createOrPlusPlus(comandsUsage, cmd)
        if 'exit' == cmd:
            desk.gaveUp()
            desk.prettyPrint()
            break
        if 'help' == cmd:
            # each cmd with [a-z] should write length of that word
            print("Type `exit` to gave up (solution and statistics will be printed)");
            print("I[a-z] to show next image (from all) for given word")
            print("T[a-z] to show next hint (from all) for given word")
            print("G[a-z] to show next hint (from all) for given word in external window")
            print("Inumber[a-z] to show Nth image (from all) for given word")
            print("Tnumber[a-z] to show Nth hint (from all) for given word")
            print("Gnumber[a-z] to show Nth hint (from all) for given word in external window")
            print("II[a-z] to show all images for given word")
            print("TT[a-z] to show all texts for given word")
            print("GG[a-z] to show all texts for given word in external window")
            generateWords.reusableHelp()
            print("newI[a-z] to generate and add new image for given word. Use all instead of a-z to generate all")
            print("newT[a-z] to generate and add new text for given word. Use all instead of a-z to generate all")
            print("delInumber[a-z] to remove Nth image. Check by In before")
            print("delTnumber[a-z] to remove Nth text. Check by Tn before")
            print("everything else is considered as guess")
            continue
        if cmd.startswith('II') or cmd.startswith('TT') or cmd.startswith('GG'):
            # FIXME show all dialogs in paralel (needs global master window)
            try:
                if processIITTGGaz(cmd, desk, lang):
                    continue
            except:
                print("XX[A-Z] expected")
                continue
        if cmd.startswith('I') or cmd.startswith('T') or cmd.startswith('G'):
            try:
                if processITGaz(cmd, desk, textIndexes, imagesIndexes, lang):
                    continue
            except:
                print("X[A-Z] expected")
                continue
        if generateWords.reusableRepl(cmd, desk):
            continue

if __name__ == "__main__":
    main()
