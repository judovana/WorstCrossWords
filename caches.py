import pathlib
import base64
from PIL import Image

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
    r = dirr + "/"+lang+"2en"
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
    base64_bytes = base64_string.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string

def getNameForAiCache(word, counter, suffix):
    return _encode(salt1+word+str(counter))+salt2+suffix

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
    
