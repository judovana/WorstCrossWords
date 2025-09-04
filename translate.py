import sys
from transformers import M2M100ForConditionalGeneration
from tokenization_small100 import SMALL100Tokenizer

initialized=False
articles = {'a': '', 'an':'', 'and':'', 'the':''}


def removearticles(text):
    rest = []
    for word in text.split():
        if word not in articles:
            rest.append(word)
    return ' '.join(rest)

def initialize():
    global model
    model = M2M100ForConditionalGeneration.from_pretrained("alirezamsh/small100")
    global tokenizer
    tokenizer  = SMALL100Tokenizer.from_pretrained("alirezamsh/small100")
    global initialized
    initialized=True

def translateToEn(text):
    return translateTo(text, "en")

def translateTo(text, lang):
    if (not initialized):
        initialize()
    tokenizer.tgt_lang = lang
    encoded = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(**encoded)
    translated=tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    s=removearticles(translated[0].lower().strip())
    return s;

def main():
    if len(sys.argv) == 1:
        print("at last one word/sentence to transalte expected")
        sys.exit(1)
    if len(sys.argv) == 2:
        r = translateTo(sys.argv[1], "en")
        print(r)
    if len(sys.argv) > 2:
        for element in sys.argv:
            r = translateTo(element, "en")
            print(element + "->" + r)

if __name__ == "__main__":
    main()
