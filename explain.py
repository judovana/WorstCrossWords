from transformers import pipeline
import sys

initialized=False

def initialize():
    global qa_pipeline
    qa_pipeline = pipeline("text-generation", model='EleutherAI/gpt-neo-1.3B')
    initialized=True

def generate(word):
    result=generateImpl(word, True)
    result2=result.replace(word.lower(), "XXXXX")
    return result2

def generateImpl(word, rephrase):
    if (not initialized):
        initialize()
    if rephrase:
        question = "explain "+word+" in english without using word "+word
    else:
        question = word
    result = qa_pipeline(question, min_length=10, max_length=100)[0]['generated_text'].lower()
    return result

def main():
    if len(sys.argv) != 2:
        print("expects exactly one argument - description sentence")
        sys.exit(1)
    answer=generateImpl(sys.argv[1], " " not in sys.argv[1]);
    print(answer)

if __name__ == "__main__":
    main()
