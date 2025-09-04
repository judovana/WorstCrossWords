# WorstCrossWords
 * This is AI powered, multi-language, *terminal*,  worst crossword game ever created
 * it is powered by awesome `transformers` and `diffusers` by https://huggingface.co
 * I'm no python master non python enthusiastic, so I apologies for bad practices

## How it works
 * This is dummy crossword game, where the hints are provided by AI
 * You can play in any language, you only need file with words to be used, which name correspond to its language code, and can be passed to model as source language ID
   * exemplar `cs`, `de` and `en` packs are included
 * the crossword is generated in your language, and hints for individual words are provided by AI as
   * image
  * text
 * **Note, that it is like playing it with friendly alien, who really wants to help, but have really weird opinions about each word**
 * The communication with AI is exclusively in English
   * trying to pass to it queries in different language leads to absolute nonsenses
 * so:
   * each word is translated from your language to English
     * if you play in English this step is skipped 
   * then the image and textual explanation is generated
     * the explanation is translated back to your language (unless in English)
   *  obviously playing in English is much more easy, as one level of AI intervenes disappears
     * The English to English worked pretty well, so saving at least some time.
 * this is optimized to run on **CPU**. But all AI operations are costly, on pretty good CPU without GPU:
   * translation - few seconds
   * text explanation - around minute
   * image - about 5 minutes
 * With GPU it should go much faster but is for now untested

## dependencies
 * It have many dependencies, run `sh deps` to get them all.
 * each model is downloaded on first usage.
   * I recommend to try each model first as standalone (caching however do not (intentionally) work)
 * each model have around 1-2GB and are optimised for local usage on CPU
 * Feel free to replace them, based on you HW
   * eg migrating to `stable-diffusion-v1-5` for image generations moved it from minutes to days on my HW.

## individual components
Are self explaining I hope. Do not run them in parallel, each of them is very CPU intense:
 * `python translate.py "ahoj trpaslíku"`
<details>
 
```
hello puppy
```
</details>

 *  `python translate.py  zug`
<details>
 
```
tough
```
</details>

 * `python  explain.py  castle`
<details>
 
```
explain castle in english without using word castle in dutch.

a:

not sure what you mean by "english castle in dutch". i think you're talking about a castle in english, and that the castle is located in a city in dutch. 
the main difference is that in dutch castles are not castles in english, they are fortified (ie. built on a hill). the word castle in english can also refer to a building or a place, but it can be used without the "in" word.
a castle is used as a noun, as a relative, or as an adjective. the definition of a castle in english is:

a fortified structure built on a hill, often defended or defended against the sea

but if you are trying to talk about the castle being located in a certain city in dutch, then the place could be in the city in dutch or even in the city the castle is located, without the words castle in english being used. 
so your question seems to be:
how do i find all the castles in english?
```
</details>

 * `python  explain.py  "pink  car"`
<details>
 
```
pink  car-shark 
"cease to do the things you know not, 
cease to dream the things that you know not."

—from aeschylus, _seven against thebes_

so what has this got to do with my career? aeschylus is on his way to the athenian stadium, where the greatest of the city's athletic contests is being held. his audience has assembled to watch him perform a greek choral show, and they'd like him to sing a verse from his _seven against thebes_ to them.

when he was told that he couldn't actually sing the chorus, he tried it anyway. it was an effective idea: 

_now a little bird, winged like a dove,_

_catches a passing ship, takes it home_

_with it, in its nest, i say to all_

_that are the birds of heaven above,_

_come and see all the lovely sights_

_the bird has to tell us of_.
```
</details>

 * `python  generateImage.py  bus`
<details>
![bus by ai](https://github.com/user-attachments/assets/2e674011-9f6b-48ab-96b5-17e31641a8f1)
</details>
 
 * `python generateWords.py  20`
<details>
 
```
reding all interesting words in cs
Loaded 23219 words
A: 7,4> madrigal (8)
B: 8,0ˇ bysta (5)
C: 14,0ˇ dikalciumfosfát (15)
D: 10,2> vratka (6)
E: 12,0> nadhled (7)
F: 10,6> pramice (7)
G: 18,0ˇ dodavatelka (11)
H: 18,4> vozík (5)
I: 16,4ˇ ořech (5)
J: 10,6ˇ pitvorka (8)
K: 22,4ˇ klatba (6)
L: 14,14> trinitron (9)
M: 4,12> knihařka (8)
N: 8,8ˇ tečka (5)
. . . . . . . . b . . . n a d h l e d . . . . .
. . . . . . . . y . . . . . i . . . o . . . . .
. . . . . . . . s . v r a t k a . . d . . . . .
. . . . . . . . t . . . . . a . . . a . . . . .
. . . . . . . m a d r i g a l . o . v o z í k .
. . . . . . . . . . . . . . c . ř . a . . . l .
. . . . . . . . . . p r a m i c e . t . . . a .
. . . . . . . . . . i . . . u . c . e . . . t .
. . . . . . . . t . t . . . m . h . l . . . b .
. . . . . . . . e . v . . . f . . . k . . . a .
. . . . . . . . č . o . . . o . . . a . . . . .
. . . . . . . . k . r . . . s . . . . . . . . .
. . . . k n i h a ř k a . . f . . . . . . . . .
. . . . . . . . . . a . . . á . . . . . . . . .
. . . . . . . . . . . . . . t r i n i t r o n .

. . . . . . . . B . . . E E E E E E G . . . . .
. . . . . . . . B . . . . . C . . . G . . . . .
. . . . . . . . B . D D D D D D . . G . . . . .
. . . . . . . . B . . . . . C . . . G . . . . .
. . . . . . . A B A A A A A C . I . H H H H K .
. . . . . . . . . . . . . . C . I . G . . . K .
. . . . . . . . . . J F F F F F I . G . . . K .
. . . . . . . . . . J . . . C . I . G . . . K .
. . . . . . . . N . J . . . C . I . G . . . K .
. . . . . . . . N . J . . . C . . . G . . . K .
. . . . . . . . N . J . . . C . . . G . . . . .
. . . . . . . . N . J . . . C . . . . . . . . .
. . . . M M M M N M M M . . C . . . . . . . . .
. . . . . . . . . . J . . . C . . . . . . . . .
. . . . . . . . . . . . . . L L L L L L L L L .
pitvorka
ok!
. . . . . . . . B . . . E E E E E E G . . . . .
. . . . . . . . B . . . . . C . . . G . . . . .
. . . . . . . . B . D D D D D D . . G . . . . .
. . . . . . . . B . . . . . C . . . G . . . . .
. . . . . . . A B A A A A A C . I . H H H H K .
. . . . . . . . . . . . . . C . I . G . . . K .
. . . . . . . . . . p F F F F F I . G . . . K .
. . . . . . . . . . i . . . C . I . G . . . K .
. . . . . . . . N . t . . . C . I . G . . . K .
. . . . . . . . N . v . . . C . . . G . . . K .
. . . . . . . . N . o . . . C . . . G . . . . .
. . . . . . . . N . r . . . C . . . . . . . . .
. . . . M M M M N M k M . . C . . . . . . . . .
. . . . . . . . . . a . . . C . . . . . . . . .
. . . . . . . . . . . . . . L L L L L L L L L .
```
</details>

## crosswords generation issue:
Note, the generation is not perfect, and never was intended to be, so it can create things like:
```
word1word2
```
where word1 and word2 are words. (no intersection, they were connected by accident from different crossing)
or
```
word1w
     o
     r
     d
     2
```
where word1 and word2 are words. (no intersection, they were connected by accident from different crossing)
or
```
word1word2
```
where word1w (note the intersection, connected intentionally) and word2 are words
or
```
word1w
     o
     r
     d
     2
```
where word1w (note the intersection, connected intentionally) and word2 are words
Especially the `word1word2` case with intersection is very confusing, sorry.


