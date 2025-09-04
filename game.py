import translate
import generateImage
import explain
import show_image
import caches
import random
import generateWords
from PIL import Image
import pathlib
import sys

wordsFile="cs"
#wordsFile="de"

caches.loadCache(wordsFile)
words=caches.readWorlist(wordsFile)
random.shuffle(words)
word=words[0]
word="čert"
#word="sem"
print("eg " + word)
if wordsFile == "en":
    translatedId=word
    print(" -> " +  word + " (skipped)")
else:
    if word in caches.getCurrentTransCache():
        translatedId = caches.getCurrentTransCache()[word]
        if translatedId.strip() == "":
            translatedId=word;
        print(" -> " +  translatedId + " (cached)")
    else:
        translatedId=translate.translateToEn(word)
        print(" -> " +  translatedId + " (translated)")
        caches.addToCache(word, translatedId, wordsFile)

explanationFilesTransalted=caches.getFilesFromTransaltedAiExplainCache(wordsFile, translatedId)
if not explanationFilesTransalted:
    explanation=explain.generate(translatedId)
    if not wordsFile == "en":
        explanation=translate.translateTo(explanation, wordsFile)
    caches.putTextToAiTransaltedCache(wordsFile, translatedId, explanation)
    explanationFilesTransalted=caches.getFilesFromTransaltedAiExplainCache(wordsFile, translatedId)
for file in explanationFilesTransalted:
    print(file)
    print(pathlib.Path(file).read_text())


explanationImages=caches.getFilesFromAiImageCache(translatedId)
if not explanationImages:
    img = generateImage.generateImg(translatedId)
    caches.putImageToAiCache(translatedId, img);
    explanationImages=caches.getFilesFromAiImageCache(translatedId)
for file in explanationImages:
    print(file)
    show_image.display_image(file)

qhelp="exit ? ?n ?? (? ?n ?? I In II T Tn TT newI newT delIn delTn)[a-z]"
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
        print("II[a-z] to show all images for given word")
        print("TT[a-z] to show all texts for given word")
        generateWords.reusableHelp()
        print("newI[a-z] to generate and add new image for given word. Use all instead of a-z to generate all")
        print("newT[a-z] to generate and add new text for given word. Use all instead of a-z to generate all")
        print("delInumber[a-z] to remove Nth image. Check by In before")
        print("delTnumber[a-z] to remove Nth text. Check by Tn before")
        print("everything else is considered as guess")
print("solved crossword:")
