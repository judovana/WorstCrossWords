import caches
import random
import sys

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
                ch=wwp.word[indexes[0]]
                if wwp.direction==">":
                    y=wwp.y; x=wwp.x+indexes[0]
                if wwp.direction=="ˇ":
                    y=wwp.y+indexes[0]; x=wwp.x
                self.desk[y][x]=ch
                wwp.found[indexes[0]] = True;
                return wwp.word[indexes[0]]+" at "+str(x)+","+str(y);
        return "Puzzle solved!"

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
    desk=init(15, 24)
    wordsWithPlacement = []
    word=words.pop();
    # to place first randmly w/h is changing the order in theb elow loop...
    initx=int(random.randint(0, len(desk[0])-len(word)-2)/2)*2
    inity=int(random.randint(0, len(desk)-2)/2)*2
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

Amark=65
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
    if cmd.startswith('??'):
        ret=desk.helpWord(letterToId(cmd[2:].upper()));
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

def main():
    print("optional first argument is number of words. Optional second argument may follow, file with all words")
    wcount=10
    if len(sys.argv) > 1:
        wcount=int(sys.argv[1])
    wordFile="cs"
    if len(sys.argv) > 2:
        wordFile=sys.argv[2]
    words=caches.readWorlist(wordFile)
    random.shuffle(words)
    desk=generate(words, wcount)
    cheat(desk)
    desk.prettyPrint()
    print()
    desk.hideAll()
    desk.prettyPrint()
    for line in sys.stdin:
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

