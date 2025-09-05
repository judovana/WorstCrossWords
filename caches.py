import pathlib
import base64
import sys
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
from datetime import datetime

noTranslationLang="en"
cacheDir="cache"
transCache = {}
doLog = True

def _log(s):
    if doLog:
        print(s)

def readWorlist(file):
    print("reding all interesting words in " + file)
    words = [];
    with open(file, 'r') as file:
        for line in file:
            words.append(line.strip().lower())
    print("Loaded " + str(len(words) )+ " words")
    return words

def checkAndCreateDir(file):
    if pathlib.Path(file).exists():
        pass
    else:
        pathlib.Path(file).mkdir(parents=True, exist_ok=True)
  
def checkAndCreateFile(file):
    if pathlib.Path(file).exists():
        pass
    else:
        with open(file, 'w') as f:
            pass 

def getTransCacheFile(lang):
    dirr=cacheDir+"/transaltions"
    r = dirr + "/"+lang+"2"+noTranslationLang
    checkAndCreateDir(dirr)
    checkAndCreateFile(r)
    return r

def getImgCacheDir():
    r=cacheDir+"/images"
    checkAndCreateDir(r)
    return r

def getExplanationsCacheDir():
    r=cacheDir+"/explanations"
    checkAndCreateDir(r)
    return r

def getTransaltedExplanationsCacheDir(lang):
    r=getExplanationsCacheDir()+"/"+lang
    checkAndCreateDir(r)
    return r

def getCurrentTransCache():
    return transCache

def loadCache(lang):
    global transCache
    transCache = {}
    _log("reding "+getTransCacheFile(lang) + " cache")
    with open(getTransCacheFile(lang), 'r') as file:
        for line in file:
            line=line.strip()
            transCache[line.split(":")[0]] = line.split(":")[1]
    _log("Loaded " + str(len(transCache))+ " cache items")

def addToCache(key, value, lang):
    global transCache
    transCache[key] = value;
    with open(getTransCacheFile(lang), "w") as f:
        for k, v in transCache.items():
               f.write(k+":"+v+"\n")
    _log("saved " + str(len(transCache))+ " items to cache")

def getFilesFromAiExplainCache(word):
    return getFilesFromAiCache(getExCacheFile(), word, ".txt")

def getFilesFromTransaltedAiExplainCache(lang, word):
    return getFilesFromAiCache(getTransaltedExplanationsCacheDir(lang), word, ".txt")

def getFilesFromAiImageCache(word):
    return getFilesFromAiCache(getImgCacheDir(), word, ".jpg")

def getFreeFileForAiExplainCache(word):
    return getFreeFileForAiCache(getExCacheFile(), word, ".txt")

def getFreeFileForTrasnaltedAiExplainCache(lang, word):
    return getFreeFileForAiCache(getTransaltedExplanationsCacheDir(lang), word, ".txt")

def getFreeFileForAiImageCache(word):
    return getFreeFileForAiCache(getImgCacheDir(), word, ".jpg")

def putTextToAiCache(word, content):
    return putTextToAiCache(getExCacheFile(), word, content)

def putTextToAiTransaltedCache(lang, word, content):
    return putTextToAiCache(getTransaltedExplanationsCacheDir(lang), word, content)

def putImageToAiCache(word, img):
    return putImageToAiCacheImpl(getImgCacheDir(), word, img)

salt1="sdfuikloghdffkl"
salt2="shkhilkdfseyula"

def _encode(sample_string):
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def _decode(sample_string):
    sample_string_bytes = sample_string.encode("ascii")
    sample_string_bytes = base64.b64decode(sample_string_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string

def getNameForAiCache(word, counter, suffix):
    return _encode(salt1+word+str(counter))+salt2+suffix

def getNameFromAiCache(fileName, suffix):
    fileName=fileName.replace(salt2+suffix,"")
    fileName=_decode(fileName)
    return fileName.replace(salt1,"").replace(salt2,"")

def getFilesFromAiCache(dir, word, suffix):
    usedFiles = [];
    for x in range(1, 1000):
        file=dir+"/"+getNameForAiCache(word, x, suffix)
        if pathlib.Path(file).exists():
            usedFiles.append(file);
    _log("Found " + str(len(usedFiles))+ " cached items for " + word + " in " + dir)
    return usedFiles

def getFreeFileForAiCache(dir, word, suffix):
    for x in range(1, 1000):
        file=dir+"/"+getNameForAiCache(word, x, suffix)
        if not pathlib.Path(file).exists():
            return file;
    return "Error, cache full";


def putTextToAiCache(dir, word, content):
    file = getFreeFileForAiCache(dir, word, ".txt")
    with open(file, "w") as f:
        f.write(content)
    _log("cached text for " + word + " in " + file)
    return file

def putImageToAiCacheImpl(dir, word, img):
    file = getFreeFileForAiCache(dir, word, ".jpg")
    img.save(file)
    _log("cached image for " + word + " in " + file)
    return file
    
def main():
    if len(sys.argv) == 3 and (sys.argv[2] == "print" or sys.argv[2] == "show" or sys.argv[2] == "read"):
        lang=sys.argv[1]
        print("Translation cache content for " + lang)
        loadCache(lang)
        print(str(len(transCache))+" items")
        for k, v in transCache.items():
               print("  '"+k+"' to en is : "+v)
        exCachDir=getTransaltedExplanationsCacheDir(lang);
        print("Explanations cache for " + lang+ " is " + exCachDir)
        files = [f for f in listdir(exCachDir)]
        print(str(len(files))+" items")
        for f in files:
               print("  '"+getNameFromAiCache(f, ".txt")+"'("+str(os.path.getsize(exCachDir+"/"+f))+"b)"+" saved as: "+f)
        immCachDir=getImgCacheDir();
        print("Image cache (shared for al languages)  is " + immCachDir)
        files = [f for f in listdir(immCachDir)]
        print(str(len(files))+" items")
        for f in files:
               print("  '"+getNameFromAiCache(f, ".jpg")+"'("+str(os.path.getsize(immCachDir+"/"+f))+"b)"+" saved as: "+f)
        sys.exit(0)
    if len(sys.argv) < 4:
        print("first argument - language (eg cs, en or de), for which ")
        print("second argument - number of iterations. How many explanations and images you want for each word")
        print("third argument - input file - for each line in this file an image(s) and explanation(s) and transaltions (if non en)")
        print("xor, third (and any following argument) are simply input words to cache")
        print("Warning. Items are added to caches. No old items are discarded, nor replaced. If you had one `eye` there, and you add `eye` with two iterations in same lanf, there  will be three")
        print("Warning. Thetranslation cache however is reused, and onl new words are added")
        print("you can use also `lang` `print` magical command to print caches")
        sys.exit(1)
    lang=sys.argv[1]
    iterations=int(sys.argv[2])
    words=sys.argv[3:]
    if pathlib.Path(sys.argv[3]).exists():
        words=readWorlist(sys.argv[3])
    totalCount=iterations*len(words)
    total=0
    startStamp=datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
    for iteration in range(0, iterations):
        for word in words:
            total+=1
            word=word.lower()
            print(str(total)+"/"+str(totalCount)+" " + word + "("+str(iteration+1)+")")
    stopStamp=datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
    print("done: "+startStamp+" - "+stopStamp)
    
if __name__ == "__main__":
    main()
