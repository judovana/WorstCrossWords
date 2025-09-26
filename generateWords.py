import random
import sys
import re
import os
import cmd

SIZE_VAR="SIZE"
RECYCLE_VAR="RECYCLE"
recycle=True
if os.environ.get(RECYCLE_VAR) == "False":
  recycle=False

def readWorlist(file):
    print("reding all interesting words in " + file)
    words = [];
    with open(file, 'r') as file:
        for line in file:
            words.append(line.strip().lower())
    print("Loaded " + str(len(words) )+ " words")
    return words

def substringIndexes(pattern, text):
    return [m.start() for m in re.finditer(pattern, text)]

class DeskWithWords:
    def __init__(self, wordsWithPlacement, desk):
        self.wordsWithPlacement = wordsWithPlacement
        self.desk = desk

    def width(self):
        return len(self.desk[0])

    def hideAll(self):
        for index,wwp in enumerate(self.wordsWithPlacement):
            wwp.hideAll()
            if wwp.direction==">":
                for i, character in enumerate(wwp.word):
                    self.desk[wwp.y][wwp.x+i]=idToLetter(index)
            if wwp.direction=="ˇ":
                for i, character in enumerate(wwp.word):
                    self.desk[wwp.y+i][wwp.x]=idToLetter(index)

    def prettyPrint(self):
        for y in self.desk:
            print(" ".join(y))

    def length(self, intId):
        if len(self.wordsWithPlacement)<=intId or intId <0 :
            return "There is just " + str(len(self.wordsWithPlacement)) + " words: " +  idToLetter(0) + "-"+idToLetter(len(self.wordsWithPlacement)-1)
        return "Length of "+idToLetter(intId) + " is " + str(len(self.wordsWithPlacement[intId].word))

    def guesSubstringEverywhere(self, substring):
        counter = 0
        for word in self.wordsWithPlacement:
            if word.revealPattern(substring):
                counter+=1
            self.fixWord(word)
        return "injected: " + str(counter)+"x"

    def guesSubstringIn(self, intId, substring):
        if len(self.wordsWithPlacement)<=intId or intId < 0:
            return "There is just " + str(len(self.wordsWithPlacement)) + " words: " +  idToLetter(0) + "-"+idToLetter(len(self.wordsWithPlacement)-1)
        if self.wordsWithPlacement[intId].revealPattern(substring):
            self.fixWord(self.wordsWithPlacement[intId])
            return "success!"
        else:
            return "nope"

    def solve(self, word):
        hit=False
        for index, wwp in enumerate(self.wordsWithPlacement):
            if wwp.word == word:
                wwp.showAll()
                hit=True
                if wwp.direction==">":
                    for i, character in enumerate(wwp.word):
                        self.desk[wwp.y][wwp.x+i]=character
                if wwp.direction=="ˇ":
                    for i, character in enumerate(wwp.word):
                        self.desk[wwp.y+i][wwp.x]=character
        return hit
    
    def gaveUp(self):
        for index, wwp in enumerate(self.wordsWithPlacement):
                wwp.showAll()
                if wwp.direction==">":
                    for i, character in enumerate(wwp.word):
                        self.desk[wwp.y][wwp.x+i]=character
                if wwp.direction=="ˇ":
                    for i, character in enumerate(wwp.word):
                        self.desk[wwp.y+i][wwp.x]=character

    def helpRandomLetter(self):
        wwpCopy=list(self.wordsWithPlacement)
        random.shuffle(wwpCopy)
        for index, wwp in enumerate(wwpCopy):
            indexes=[]
            for i, boool in enumerate(wwp.found):
                if not boool:
                    indexes.append(i)
            if len(indexes) > 0:
                random.shuffle(indexes)
                return self.fillLetterInWord(wwp, indexes[0])
        return "Puzzle solved!"

    def fillLetterInWord(self, wwp, index):
        ch=wwp.word[index]
        if wwp.direction==">":
            y=wwp.y; x=wwp.x+index
        if wwp.direction=="ˇ":
            y=wwp.y+index; x=wwp.x
        self.desk[y][x]=ch
        wwp.found[index] = True;
        return wwp.word[index]+" at "+str(x)+","+str(y);

    def showWord(self, wwp):
        wwp.showAll();
        self.fixWord(wwp)

    #todo reuse on more places
    def fixWord(self, wwp):
        if wwp.direction==">":
            for i, character in enumerate(wwp.word):
                if wwp.found[i]:
                    self.desk[wwp.y][wwp.x+i]=character
        if wwp.direction=="ˇ":
            for i, character in enumerate(wwp.word):
                if wwp.found[i]:
                    self.desk[wwp.y+i][wwp.x]=character

    def helpRandomWord(self):
        wwpCopy=list(self.wordsWithPlacement)
        random.shuffle(wwpCopy)
        for index, wwp in enumerate(wwpCopy):
            if wwp.isFullyShown():
                continue
            else:
                self.showWord(wwp)
                return wwp.word+" at "+str(wwp.x)+","+str(wwp.y);
        return "Puzzle solved!"

    def helpWord(self, index):
        wwp = self.wordsWithPlacement[index]
        self.showWord(wwp)
        return wwp.word+" at "+str(wwp.x)+","+str(wwp.y);

    def helpExactLetter(self, numLet):
        print(numLet)
        firstLetter=numLet[0]
        lastLetter=numLet[-1]
        #?number to fill random Nth letter")        
        if firstLetter.isnumeric() and lastLetter.isnumeric():
            return self.helpExactLetterInRandomWord(int(numLet))
        #?[a-z] to fill random letter of selected word")
        if (not firstLetter.isnumeric()) and (not lastLetter.isnumeric()):
            return self.helpRandomLetterInExactWord(letterToId(firstLetter))
        #?number[a-z] to fill Nth letter of selected word")
        if firstLetter.isnumeric() and (not lastLetter.isnumeric()):
            return self.helpExactLeterInExactWord(int(re.sub('[^0-9]+', '', numLet)), letterToId(re.sub('[0-9]+', '', numLet)[0]))
        if lastLetter.isnumeric() and (not firstLetter.isnumeric()):
            return self.helpExactLeterInExactWord(int(re.sub('[^0-9]+', '', numLet)), letterToId(re.sub('[0-9]+', '', numLet)[0]))
        return "expected ?[A-Z] or ?[0-9]+ or ?[0-9][A-Z]"
        
    def helpExactLetterInRandomWord(self, letterIdInt):
        letterIdInt=letterIdInt-1
        wwpCopy=list(self.wordsWithPlacement)
        random.shuffle(wwpCopy)
        for index, wwp in enumerate(wwpCopy):
            if letterIdInt<len(wwp.found) and wwp.found[letterIdInt] == False:
                return self.fillLetterInWord(wwp, letterIdInt)
        return "Puzzle solved?"

    def helpRandomLetterInExactWord(self, wordIdInt):
        if (wordIdInt>=len(self.wordsWithPlacement) or wordIdInt <0):
            return "there is only "+str(len(self.wordsWithPlacement)-1)+" words"
        wwp=self.wordsWithPlacement[wordIdInt]
        indexes=[]
        for i, boool in enumerate(wwp.found):
            if not boool:
                indexes.append(i)
        if len(indexes) > 0:
            random.shuffle(indexes)
            return self.fillLetterInWord(wwp, indexes[0])
        return "Word filled?"

    def helpExactLeterInExactWord(self, letterIdInt, wordIdInt):
        if (wordIdInt>=len(self.wordsWithPlacement) or wordIdInt <0):
            return "there is only "+str(len(self.wordsWithPlacement)-1)+" words"
        word=self.wordsWithPlacement[wordIdInt]
        if (letterIdInt>len(word.word)):
            return "word "+idToLetter(wordIdInt)+"  have "+str(len(word.word))+" chars"
        return self.fillLetterInWord(word, letterIdInt-1)

class WordWithPlacement:
    def __init__(self, x, y, word, direction):
        self.x = x
        self.y = y
        self.word = word
        self.direction=direction
        self.found = []
        for index, character in enumerate(self.word):
                self.found.append(True)
    def visibility(self):
        r=""
        for state in self.found:
            if state:
                r+="t"
            else:
                r+="f"
        return r

    def hideAll(self):
        for index, character in enumerate(self.word):
            self.found[index]=False

    def showAll(self):
        for index, character in enumerate(self.word):
            self.found[index]=True

    def isFullyHidden(self):
        sset = {e for e in self.found}
        return len(sset)==1 and sset.pop() == False

    def revealPattern(self, pattern):
        indexes = substringIndexes(pattern, self.word)
        if (len(indexes) <=0):
            return False
        for index in indexes:
            for x in range(index, index+len(pattern)):
                self.found[x]=True
        return True

    def isFullyShown(self):
        sset = {e for e in self.found}
        return len(sset)==1 and sset.pop() == True

    def toStr(self):
        return str(self.x)+","+str(self.y)+self.direction+" " + self.word + " ("+str(len(self.word))+") - " + self.visibility()

def init(width, height):
    desk=[]
    for y in range(0, width):
        a=[]
        desk.append(a);
        for x in range(0, height):
            #a.append("x"+str(x)+"y"+str(y));
            a.append(".");
    return desk

def popik(words):
    word = words.pop()
    if recycle:
        words=[word]+words
    return word; 

def generate(words, maxWords):
    userWidth=15
    userHeight=24
    if os.environ.get(SIZE_VAR):
        userWidth=int(re.sub("x.*", "", os.environ.get(SIZE_VAR)))
        userHeight=int(re.sub(".*x", "", os.environ.get(SIZE_VAR)))
    desk=init(userWidth, userHeight)
    wordsWithPlacement = []
    word=popik(words)
    # to place first randmly w/h is changing the order in theb elow loop...
    while True:
        LX=len(desk[0])-len(word)-2
        if (LX<0):
            word=popik(words);
            continue
        initx=int(random.randint(0, LX)/2*2)
        break
    LY=len(desk)-2
    if LY<0:
       LY=0
    inity=int(random.randint(0, LY)/2*2)
    placeHor(desk, initx, inity, word);
    wordsWithPlacement.append(WordWithPlacement(initx,inity,word, ">"))
    maxIterations=0
    origLenWords=len(words)*3
    while len(wordsWithPlacement)<maxWords and maxIterations < origLenWords and len(words) > 1: #two pops in below
        maxIterations+=1
        word=popik(words);
        placed=False
        for y in range(0, len(desk), 2):
            for x in range(0, len(desk[y]), 2):    
                if canPlaceVer(desk, x, y, word):
                    placeVer(desk, x, y, word);
                    wordsWithPlacement.append(WordWithPlacement(x,y,word, "ˇ"))
                    word=popik(words);
                    placed=True
                    break
            if placed:
                break
        for y in range(0, len(desk), 2):
            for x in range(0, len(desk[y]), 2):    
                if canPlaceHor(desk, x, y, word):
                    placeHor(desk, x, y, word);
                    wordsWithPlacement.append(WordWithPlacement(x,y,word, ">"))    
                    placed=True
                    break
            if placed:
                break
    print(str(maxIterations)+"/"+str(maxWords)+ " - " + str(recycle))
    return DeskWithWords(wordsWithPlacement, desk)

def placeHor(desk, x, y, word):
    for index, character in enumerate(word):
        desk[y][x+index]=character

def placeVer(desk, x, y, word):
    for index, character in enumerate(word):
        desk[y+index][x]=character

def canPlaceHor(desk, x, y, word):
    if len(word)+x > len(desk[y]):
        return None
    intersections=0
    for index, character in enumerate(word):
        placeStatus=isFree(desk, x+index, y, character)
        if placeStatus>=0:
            intersections+=placeStatus
            continue
        else:
            return None
    if (intersections>0):
        return word
    else:
        return None

def canPlaceVer(desk, x, y, word):
    if len(word)+y > len(desk):
        return None
    intersections=0;
    for index, character in enumerate(word):
        placeStatus=isFree(desk, x, y+index, character)
        if placeStatus>=0:
            intersections+=placeStatus
            continue
        else:
            return None
    if (intersections>0):
        return word
    else:
        return None

def isFree(desk, x, y, invasiveChar):
    char = desk[y][x]
    #word can be put on epty palace  OR on same letter
    if (char == "" or char == " " or char == "."  or char == "-"  or char == "_"):
        return 0
    if char == invasiveChar:
        return 1
    return -1;

Amark=ord("A") #65
def idToLetter(i):
    return chr(i+Amark)    

def letterToId(i):
    return ord(i)-Amark

def cheat(desk):
    for index,wwp in enumerate(desk.wordsWithPlacement):
        print(idToLetter(index)+": "+wwp.toStr())

def reusableRepl(cmd, desk) :
    if '' == cmd:
        desk.prettyPrint()
        return True    
    if 'cheat' == cmd:
        cheat(desk)
        return True
    if '?' == cmd:
        ret=desk.helpRandomLetter();
        print(ret)
        desk.prettyPrint()
        return True
    if '??' == cmd:
        ret=desk.helpRandomWord();
        print(ret)
        desk.prettyPrint()
        return True
    if (cmd.startswith('l') or cmd.startswith('L')) and len(cmd)==2:
        print(desk.length(letterToId(cmd[1:].upper())))
        desk.prettyPrint()
        return True
    if cmd.startswith('sub'):
        cmd=re.sub("sub *", "", cmd)
        ops=re.split(" +", cmd)
        if len(ops)==1:
            print(desk.guesSubstringEverywhere(ops[0]))
        if len(ops)>1:
            print(desk.guesSubstringIn(letterToId(ops[0][0].upper()), ops[1]))
        desk.prettyPrint()
        return True
    if cmd.startswith('??'):
        try:
            ret=desk.helpWord(letterToId(cmd[2:].upper()));
            print(ret)
        except:
            print("??[A-Z] expected")
        desk.prettyPrint()
        return True
    if cmd.startswith('?'):
        strip=cmd[1:].upper()
        ret=desk.helpExactLetter(strip);
        print(ret)
        desk.prettyPrint()
        return True
    hit=desk.solve(cmd);
    if hit:
        print("ok!")
    else:
        print("nope:(")
    desk.prettyPrint()
    return True;

def reusableHelp():
        print("? to fill random letter")
        print("?number to fill random Nth letter")
        print("?[a-z] to fill random letter of selected word")
        print("?number[a-z] to fill Nth letter of selected word")
        print("?? to random whole word")
        print("??[a-z] to fill whole word of given word")
        print("L[a-z] length of given word")
        print("`sub[A-Z] guess` try to fill matching guess SUBSTRING to selected word")
        print("`sub guess` try to fill matching guess SUBSTRING to ALL words (")

def qhelp():
    print ("L ? ?number ?[a-z] ?number[a-z] ?? ??[a-z] `sub[A-Z] guess` help exit giveup")

class CmdMainShell(cmd.Cmd):
    prompt = '$ '

    def __init__(self, desk):
        super().__init__()
        self.desk=desk

    def onecmd(self, line):
        qhelp()
        cmd=line.strip()
        if 'exit' == cmd:
            self.desk.gaveUp()
            return True
        if 'giveup' == cmd.lower():
            self.desk.gaveUp()
            self.desk.prettyPrint()
            return True
        if 'help' == cmd:
            print("Type `exit` to gave up (solution will be printed)");
            print("Type `cheat` to reprint all words");
            reusableHelp()
            print("everything else is considered as guess")
            return False
        if reusableRepl(cmd, self.desk):
            return False
        return False


def main():
    print("mandatory first argument is  argument file with all words. Optional second argument may follow - number of words.") 
    print("environment variable "+SIZE_VAR+" in format WxH may be used to set size of  desk (be carefull)") 
    print("environment variable "+RECYCLE_VAR+"=False will disable recycling of words. Useful - necessary -  for huge vocabularies") 
    wordFile=None
    if len(sys.argv) <= 1:
        print("You must specify file to read words from")
        sys.exit(2)
    if len(sys.argv) > 1:
        wordFile=sys.argv[1]
    wcount=10
    if len(sys.argv) > 2:
        wcount=int(sys.argv[2])
    words=readWorlist(wordFile)
    random.shuffle(words)
    desk=generate(words, wcount)
    cheat(desk)
    desk.prettyPrint()
    print()
    desk.hideAll()
    desk.prettyPrint()
    qhelp()
    CmdMainShell(desk).cmdloop()

if __name__ == "__main__":
    main()

