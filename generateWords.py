import random
import sys
import re
import os

SIZE_VAR="SIZE"

def readWorlist(file):
    print("reding all interesting words in " + file)
    words = [];
    with open(file, 'r') as file:
        for line in file:
            words.append(line.strip().lower())
    print("Loaded " + str(len(words) )+ " words")
    return words

class DeskWithWords:
    def __init__(self, wordsWithPlacement, desk):
        self.wordsWithPlacement = wordsWithPlacement
        self.desk = desk

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
        if len(self.wordsWithPlacement)<=intId:
            return "There is just " + str(len(self.wordsWithPlacement)) + " words: " +  idToLetter(0) + "-"+idToLetter(len(self.wordsWithPlacement)-1)
        return "Length of "+idToLetter(intId) + " is " + str(len(self.wordsWithPlacement[intId].word))

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
        if wwp.direction==">":
            for i, character in enumerate(wwp.word):
                self.desk[wwp.y][wwp.x+i]=character
        if wwp.direction=="ˇ":
            for i, character in enumerate(wwp.word):
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
        if (wordIdInt>=len(self.wordsWithPlacement)):
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
        if (wordIdInt>=len(self.wordsWithPlacement)):
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

def generate(words, maxWords):
    userWidth=15
    userHeight=24
    if os.environ.get(SIZE_VAR):
        userWidth=int(re.sub("x.*", "", os.environ.get(SIZE_VAR)))
        userHeight=int(re.sub(".*x", "", os.environ.get(SIZE_VAR)))
    desk=init(userWidth, userHeight)
    wordsWithPlacement = []
    word=words.pop();
    # to place first randmly w/h is changing the order in theb elow loop...
    while True:
        LX=len(desk[0])-len(word)-2
        if (LX<0):
            word=words.pop();
            continue
        initx=int(random.randint(0, LX)/2*2)
        break
    LY=len(desk)-2
    if LY<0:
       LY=0
    inity=int(random.randint(0, LY)/2*2)
    placeHor(desk, initx, inity, word);
    wordsWithPlacement.append(WordWithPlacement(initx,inity,word, ">"))
    while maxWords > 0 and len(words) > 1: #two pops in below
        maxWords-=1
        word=words.pop();
        placed=False
        for y in range(0, len(desk), 2):
            for x in range(0, len(desk[y]), 2):    
                if canPlaceVer(desk, x, y, word):
                    placeVer(desk, x, y, word);
                    wordsWithPlacement.append(WordWithPlacement(x,y,word, "ˇ"))
                    word=words.pop();
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

def main():
    print("optional first argument is  argument file with all words. Optional second argument may follow - number of words.") 
    print("environment variable "+SIZE_VAR+" in format WxH may be used to set size of  desk (be carefull)") 
    wordFile="cs"
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
    qhelp="L ? ?number ?[a-z] ?number[a-z] ?? ??[a-z] help exit"
    print(qhelp)
    for line in sys.stdin:
        print(qhelp)
        cmd=line.strip()
        if 'exit' == cmd:
            desk.gaveUp()
            desk.prettyPrint()
            break
        if 'help' == cmd:
            print("Type `exit` to gave up (solution will be printed)");
            print("Type `cheat` to reprint all words");
            reusableHelp()
            print("everything else is considered as guess")
            continue
        if reusableRepl(cmd, desk):
            continue

if __name__ == "__main__":
    main()

