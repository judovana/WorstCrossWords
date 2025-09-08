import show_image
import show_images
import caches
import generateWords

import traceback
import threading
import random
from PIL import Image
import pathlib
import sys
import re
import os
import tkinter as tk
from tkinter import *

WRAP_ENV="WRAP"
WRAP=80
if os.environ.get(WRAP_ENV):
    wrap=int(os.environ.get(WRAP_ENV))
ASYNC_ENV="ASYNC"
ASYNC=True
if os.environ.get(ASYNC_ENV) == "False":
    ASYNC=False


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

def syncOrAsync(file, title):
        if ASYNC:
            asyncParent.queue.append(file + " " + title);
        else:
            show_image.textOrImage(file, title, WRAP)

def processInTnGnaz(cmd, desk, lang):
    intNth=re.sub('[^0-9]+', '', cmd)
    index=int(intNth)-1
    cmd=re.sub('[0-9]+', '', cmd)
    cchar=cmd[1:][0].upper()
    idInt=generateWords.letterToId(cchar)
    ccmd=cmd[:1].upper()
    if idInt >= len(desk.wordsWithPlacement):
        print("We have  have only " + str(len(desk.wordsWithPlacement))+" words")
        return True
    word=desk.wordsWithPlacement[idInt].word
    acro=''.join([cchar*len(word)])
    title=acro + " (" + str(len(word)) + ")";
    if ccmd == "T":
        allFiles=getAllExplanationsFilesFor(word, lang)
        if index >= len(allFiles) or index < 0:
            print(cchar + " have only 1-" + str(len(allFiles))+" items")
        else:
            print(title +" " + str(index+1)+"/"+str(len(allFiles)))
            print(pathlib.Path(allFiles[index]).read_text())
        return True
    if ccmd == "G":
        allFiles=getAllExplanationsFilesFor(word, lang)
        if index >= len(allFiles) or index < 0:
            print(cchar + " have only 1-" + str(len(allFiles))+" items")
        else:
            syncOrAsync(allFiles[index], title+" " + str(index+1)+"/"+str(len(allFiles)))
        return True
    if ccmd == "I":
        allFiles=getAllImageFilesFor(word, lang)
        if index >= len(allFiles) or index < 0:
            print(cchar + " have only 1-" + str(len(allFiles))+" items")
        else:
            syncOrAsync(allFiles[index], title+" " + str(index+1)+"/"+str(len(allFiles)))
        return True

def processITGaz(cmd, desk, textIndexes, imagesIndexes,lang):
    cchar=cmd[1:][0].upper()
    idInt=generateWords.letterToId(cchar)
    ccmd=cmd[:1].upper()
    if idInt >= len(desk.wordsWithPlacement):
        print("We have  have only " + str(len(desk.wordsWithPlacement))+" words")
        return True
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
        syncOrAsync(allFiles[index], title+" " + str(index+1)+"/"+str(len(allFiles)))
        return True
    if ccmd == "I":
        index=createOrPlusPlus(imagesIndexes, cchar)
        allFiles=getAllImageFilesFor(word, lang)
        if index >= len(allFiles):
            index=0
            textIndexes[cchar]=0
        syncOrAsync(allFiles[index], title+" " + str(index+1)+"/"+str(len(allFiles)))
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
            syncOrAsync(file, title)
        return True
    if ccmd == "II":
        for file in getAllImageFilesFor(word, lang):
            syncOrAsync(file, title)
        return True

def task():
    #print("hello")
    asyncParent.readQueue()
    asyncParent.root.after(100, task)

class AsyncParent():

    def createAndStart(self):
        self.queue = []
        self.live=True
        self.root = Tk()
        self.root.withdraw()
        self.root.after(100, task)
        self.root.mainloop()

    def readQueue(self):
        if self.live:
            while len(self.queue)>0:
                item=self.queue.pop()
                if item == "destroy":
                    self.live=False
                    self.root.destroy()
                    break
                else:
                    fileTitle=item.split(" ")
                    img=show_images.ImgOrNote(self.root, 0, fileTitle[0], fileTitle[0], WRAP, False)
                    img.display_gui()

    def close(self):
        self.queue.append("destroy");

def main():
    print("mandadory first argument is  argument file with all words. Optional second argument may follow - number of words.") 
    print("WARNING the language is deducted from filename - eg cs-123 will be interpreted as cs. 09de-bad will be interpreted as de and so on") 
    print("WARNING the language is detected from file name. Be sure the only letters in the filename are identifying the lang as `cs` `en` or `de`") 
    print("Warning. environment vat "+caches.NOTRANS_VAR+"set to True, will skipp transaltion step.Note it may corrupt the caches, backup them before. Noe the AI being asked for different, then english words is weird")
    print("environment variable "+generateWords.SIZE_VAR+" in format WxH may be used to set size of  desk (be carefull)") 
    print("environment variable "+ASYNC_ENV+"=False removes ability to show more images in parallel )may be better playgame actually)") 
    print("environment variable "+WRAP_ENV+"=number is setting the forced wrap for text windows") 
    wordsFile="cs"
    if len(sys.argv) <= 1:
        print("You must specify file to read words from")
        sys.exit(2)
    if ASYNC:
        global asyncParent
        asyncParent = AsyncParent()
        threading.Thread(target=asyncParent.createAndStart).start() 
    if len(sys.argv) > 1:
        wordsFile=sys.argv[1]
    wcount=5
    if len(sys.argv) > 2:
        wcount=int(sys.argv[2])
    lang=re.sub('[^a-z]+', '', wordsFile)[:2]
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
            if ASYNC:
                asyncParent.close()
            desk.gaveUp()
            desk.prettyPrint()
            break
        if 'help' == cmd:
            # each cmd with [a-z] should write length of that word
            print("Type `exit` to gave up (solution and statistics will be printed)");
            print("---- suggestions ----")
            print("I[a-z] to show next image (from all) for given word")
            print("T[a-z] to show next hint (from all) for given word")
            print("G[a-z] to show next hint (from all) for given word in external window")
            print("Inumber[a-z] to show Nth image (from all) for given word")
            print("Tnumber[a-z] to show Nth hint (from all) for given word")
            print("Gnumber[a-z] to show Nth hint (from all) for given word in external window")
            print("II[a-z] to show all images for given word")
            print("TT[a-z] to show all texts for given word")
            print("GG[a-z] to show all texts for given word in external window")
            print("---- operations and actions ----")
            generateWords.reusableHelp()
            print("---- calls to AI models ----")
            print("newsI[a-z] to generate and add new image for given word. Use all instead of a-z to generate all - sync")
            print("newsT[a-z] to generate and add new text for given word. Use all instead of a-z to generate all - sync")
            print("newI[a-z] to generate and add new image for given word. Use all instead of a-z to generate all - async")
            print("newT[a-z] to generate and add new text for given word. Use all instead of a-z to generate all - async")
            print("delInumber[a-z] to remove Nth image. Check by In before")
            print("delTnumber[a-z] to remove Nth text. Check by Tn before")
            print("everything else is considered as guess (and dont forget sub!)")
            continue
        if cmd.startswith('II') or cmd.startswith('TT') or cmd.startswith('GG'):
            # FIXME show all dialogs in paralel (needs global master window)
            try:
                if processIITTGGaz(cmd, desk, lang):
                    continue
            except:
                traceback.print_exc()
                print("XX[A-Z] expected")
                continue
        if cmd.startswith('I') or cmd.startswith('T') or cmd.startswith('G'):
            if re.match(".*[0-9].*", cmd)  == None:
                try:
                    if processITGaz(cmd, desk, textIndexes, imagesIndexes, lang):
                        continue
                except:
                    traceback.print_exc()
                    print("X[A-Z] expected")
                    continue
            else:
                if processInTnGnaz(cmd, desk, lang):
                    continue
                print("Xn[A-Z] expected")
                continue
        if cmd.startswith('newsI') or cmd.startswith('newsT'):
            if len(cmd)<6:
                print("missing ID of word")
                continue
            ccmd=cmd[:5]
            idL=cmd[5:][0].upper()
            idInt=generateWords.letterToId(idL)
            if idInt >= len(desk.wordsWithPlacement):
                print("We have  have only " + str(len(desk.wordsWithPlacement))+" words")
                continue
            word=desk.wordsWithPlacement[idInt].word
            translatedId=caches.getTranslated(lang, word)
            if ccmd == "newsT":
                explanationFilesTransaltedOld=caches.getFilesFromTransaltedAiExplainCache(lang, translatedId)
                print(idL+" now have " + str(len(explanationFilesTransaltedOld))+" expanations. Please wait for next")
                file=caches.explainToCache(lang, translatedId)
                explanationFilesTransaltedOld=caches.getFilesFromTransaltedAiExplainCache(lang, translatedId)
                print(idL+" finally have " + str(len(explanationFilesTransaltedOld))+" expanations")
                print(pathlib.Path(file).read_text())
                title=file
                for nwIndex, item in enumerate(explanationFilesTransaltedOld):
                    if item == file:
                        title= idL+idL+idL+ " "+str(nwIndex)+"/"+str(len(explanationFilesTransaltedOld))
                syncOrAsync(file, title)
            if ccmd == "newsI":
                explanationImagesOld=caches.getFilesFromAiImageCache(translatedId)
                print(idL+" now have " + str(len(explanationImagesOld))+" images. Please wait for next")
                file=caches.imageToCache(translatedId)
                explanationImagesOld=caches.getFilesFromAiImageCache(translatedId)
                print(idL+" finally have " + str(len(explanationImagesOld))+" images")
                title=file
                for nwIndex, item in enumerate(explanationImagesOld):
                    if item == file:
                        title= idL+idL+idL+ " "+str(nwIndex)+"/"+str(len(explanationImagesOld))
                syncOrAsync(file, title)
            continue
        if cmd.startswith('newI') or cmd.startswith('newT'):
            print("new async image not yet implemented - run `caches.py` for now")
            continue
        if cmd.startswith('delI') or cmd.startswith('delT'):
            intNth=re.sub('[^0-9]+', '', cmd)
            index=int(intNth)-1
            cmd=re.sub('[0-9]+', '', cmd)
            if len(cmd)<5:
                print("missing ID of word")
                continue
            idL=cmd[4:][0].upper()
            idInt=generateWords.letterToId(idL)
            ccmd=cmd[:4]
            print(ccmd)
            if idInt >= len(desk.wordsWithPlacement):
                print("We have  have only " + str(len(desk.wordsWithPlacement))+" words")
                continue
            word=desk.wordsWithPlacement[idInt].word
            translatedId=caches.getTranslated(lang, word)
            if ccmd == "delI":
                print("will delete image " +  str(index+1) + " of " + idL)
                files = explanationFilesTransaltedOld=caches.getFilesFromAiImageCache(translatedId)
            if ccmd == "delT":
                print("will delete explanation " +  str(index+1) + " of " + idL + " in " + lang)
                files = explanationFilesTransaltedOld=caches.getFilesFromTransaltedAiExplainCache(lang, translatedId)
            if len(files) <= index:
                print("in cache is only " + str(len(files)) + "items")
                continue 
            file=files[index]
            print("would delete " + file)
            continue
        if generateWords.reusableRepl(cmd, desk):
            continue

if __name__ == "__main__":
    main()



