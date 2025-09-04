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
                    self.desk[wwp.y][wwp.x+i]=chr(index+65);
            if wwp.direction=="ˇ":
                for i, character in enumerate(wwp.word):
                    self.desk[wwp.y+i][wwp.x]=chr(index+65);

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


class WordWithPlacement:
    def __init__(self, x, y, word, direction):
        self.x = x
        self.y = y
        self.word = word
        self.direction=direction
        self.found = []
        for index, character in enumerate(self.word):
                self.found.append(True)

    def hideAll(self):
        for index, character in enumerate(self.word):
            self.found[index]=False

    def showAll(self):
        for index, character in enumerate(self.word):
            self.found[index]=True

    def toStr(self):
        return str(self.x)+","+str(self.y)+self.direction+" " + self.word + " ("+str(len(self.word))+")"

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
    initx=int(random.randint(0, len(desk[0])-len(word)-1)/2)*2-1
    inity=int(random.randint(0, len(desk)-1)/2)*2
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


def main():
    words=caches.readWorlist("cs")
    random.shuffle(words)
    wcount=10
    if len(sys.argv) > 1:
        wcount=int(sys.argv[1])
    desk=generate(words, wcount)
    for index,wwp in enumerate(desk.wordsWithPlacement):
        print(chr(index+65)+": "+wwp.toStr())
    desk.prettyPrint()
    desk.hideAll()
    desk.prettyPrint()
    for line in sys.stdin:
        cmd=line.strip()
        if 'exit' == cmd:
            break
        else:
            hit=desk.solve(cmd);
            if hit:
                print("ok!")
            else:
                print("nope:(")
        desk.prettyPrint()

if __name__ == "__main__":
    main()

