import translate
import generateImage
import explain
import show_image
import caches
import generateWords

import random
from PIL import Image
import pathlib
import sys
import re

wordsFile="cs-20-2025-09-05_14:36:15"
#wordsFile="cs"
#wordsFile="de"
lang= re.sub('[^a-z]+', '', wordsFile)
print("lang is "+lang)
caches.loadCache(lang)
words=caches.readWorlist(wordsFile)
random.shuffle(words)
word=words[0]
word="čert"
#word="sem"
print("eg " + word)
translatedId=caches.getTranslated(lang, word)

explanationFilesTransalted=caches.getFilesFromTransaltedAiExplainCache(lang, translatedId)
if not explanationFilesTransalted:
    caches.explainToCache(lang, translatedId)
    explanationFilesTransalted=caches.getFilesFromTransaltedAiExplainCache(lang, translatedId)
for file in explanationFilesTransalted:
    print(file)
    print(pathlib.Path(file).read_text())

explanationImages=caches.getFilesFromAiImageCache(translatedId)
if not explanationImages:
    caches.imageToCache(lang, translatedId)
    explanationImages=caches.getFilesFromAiImageCache(translatedId)
for file in explanationImages:
    print(file)
    show_image.display_image(file)

qhelp="help exit ? ?n ?? (? ?n ?? I In II T G Tn TT GG newI newT delIn delTn)[a-z]"
history=[];
comandsUsage = {}
print(qhelp)
for line in sys.stdin:
    print(qhelp)
    cmd=line.strip()
    history.append(cmd);
    if 'exit' == cmd:
        break
    if 'help' == cmd:
        # each cmd with [a-z] should write length of that word
        print("Type `exit` to gave up (solution and statistics will be printed)");
        print("I[a-z] to show next image (from all) for given word")
        print("T[a-z] to show next hint (from all) for given word")
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
print("solved crossword:")
