import sys
import random
import caches
from datetime import datetime

def main():
    if not len(sys.argv) == 3:
        print("first argument - file to process")
        print("second argument - number of words to select")
        print("this progam will read input file, and generate new file, with N randomly selected words (which you can later cache explanations/images) for")
        sys.exit(1)
    words=caches.readWorlist(sys.argv[1])
    random.shuffle(words)
    stamp=datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
    fname=sys.argv[1]+"-"+sys.argv[2]+"-"+stamp
    with open(fname, "w") as f:
        for word in words[:int(sys.argv[2])]:
               f.write(word+"\n")
    print("Written " + sys.argv[2] + " to " +fname)
    
if __name__ == "__main__":
    main()

