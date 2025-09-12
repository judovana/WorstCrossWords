# WorstCrossWords
 * This is AI powered, multi-language, *terminal*,  worst crossword game ever created
 * it is powered by awesome `transformers` and `diffusers` by https://huggingface.co
 * I'm no python master non python enthusiastic, so I apologies for bad practices
 * [I do not need to read anymore, show me how to play](#play)
 * PRs with new cache items and words to *-cached langs welcomed

## How it works
 * This is dummy crossword game, where the hints are provided by AI
 * You can play in any language, you only need file with words to be used, which name correspond to its language code, and can be passed to model as source language ID
   * exemplar **big** `langs/cs`, `langs/de` and `langs/en` packs are included
   * exemplar `langs/cs-expert`, `langs/cs-easy` and mixture `langs/cs-cached` (for all three `cs`/`de`/`en`) are prepared, including cache so you can play out of the box
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
 * It have many dependencies, run `sh getDeps.sh` to get them all (feel free to read/adapt before running or run some parts manually)
  * it install some deps as root, some as local use (pip's). That is intentional.
  * install the non-root deps as the user which will play
  * AI models are also downloaded in this script
    * but can be later downloaded for same user local cache manually
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
<hr>

 *  `python translate.py  zug`
<details>
 
```
tough
```
</details>
<hr>

 *  `python translate.py  cs zug`
<details>
 
```
záhoda
```
</details>
<hr>

 *  `python translate.py  de okoun koza`
<details>
 
```
okoun->umgeben
koza->ziege
```
</details>
<hr>

 *  `python translate.py  en okoun koza`
<details>
 
```
okoun->admin
koza->cottage
```
Wait, realy???
</details>
<hr>

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
<hr>

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
<hr>

 * `python  generateImage.py  bus`
<details>
![bus by ai](https://github.com/user-attachments/assets/2e674011-9f6b-48ab-96b5-17e31641a8f1)
</details>
 <hr>

 * `python generateWords.py  cs 20`
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

 * `generateWords.py` can be played as separate game:
   * first argument is language file
   * second optional argument is number of words
   * it can read `$SIZE` variable rg `SIZE=5x6` to set up isze of desl
     * be carefull withboth size and number of words!
   * in runtime, the board takes several commands to help you to solve
     * see `help` in game
<hr>

 * ` python shuffle.py  cs 20`
<details>

```
reding all interesting words in cs
Loaded 23219 words
Written 20 to cs-20-2025-09-05_14:36:15
```
```
cat cs-20-2025-09-05_14\:36\:15 
dálkařka
konkurs
sypavka
primabalerína
příraz
kudlička
blaženka
plachetnice
mravouka
překládka
autoatlas
předkrm
káhira
šedesátina
podbíječka
francouzák
eiffelka
dichlorid
afganistan
barbiturát
```
</details>

   * `shuffle.py` is serving to generate subsets, which you can then pre-generate explanations and images over night and use them next morning to play (ROFL)
   <hr>

 * `python caches.py cs 2  okoun chata`
<details>

```
...
done: 2025-09-05_17:26:04 - 2025-09-05_18:11:33
okoun->admin
cache/explanations/cs/c2RmdWlrbG9naGRmZmtsYWRtaW4xshkhilkdfseyula.txt
cache/images/c2RmdWlrbG9naGRmZmtsYWRtaW4xshkhilkdfseyula.jpg
chata->chat
cache/explanations/cs/c2RmdWlrbG9naGRmZmtsY2hhdDE=shkhilkdfseyula.txt
cache/images/c2RmdWlrbG9naGRmZmtsY2hhdDE=shkhilkdfseyula.jpg
okoun->admin
cache/explanations/cs/c2RmdWlrbG9naGRmZmtsYWRtaW4yshkhilkdfseyula.txt
cache/images/c2RmdWlrbG9naGRmZmtsYWRtaW4yshkhilkdfseyula.jpg
chata->chat
cache/explanations/cs/c2RmdWlrbG9naGRmZmtsY2hhdDI=shkhilkdfseyula.txt
cache/images/c2RmdWlrbG9naGRmZmtsY2hhdDI=shkhilkdfseyula.jpg

```
note the times...
</details>

   * `caches.py` is crucial if you want to play smooth real time game.
   Use shuffle to generate susbet of your language set. Then generate cache for its content. Note, that someone can  can manually prepare translations, and so make it much more reliable (but not the player, they will know the words). Cache generation for file is eg
   * ` python caches.py  cs 5 cs-20-2025-09-05_14\:36\:15`
<details>

```
$ python caches.py  cs 5 cs-20-2025-09-05_14\:36\:15 
reding all interesting words in cs-20-2025-09-05_14:36:15
Loaded 20 words
reding cache/transaltions/cs2en cache
Loaded 12 cache items
1/100 dálkařka(1)
  Translating!
The tokenizer class you load from this checkpoint is not the same type as the class this function is called from. It may result in unexpected tokenization. 
The tokenizer class you load from this checkpoint is 'M2M100Tokenizer'. 
The class this function is called from is 'SMALL100Tokenizer'.
 -> distance (translated)
saved 13 items to cache
  Explaining!
...
done: 2025-09-05_18:21:50 - 2025-09-06_06:29:16
dálkařka->distance
cache/explanations/cs/c2RmdWlrbG9naGRmZmtsZGlzdGFuY2Uxshkhilkdfseyula.txt
cache/images/c2RmdWlrbG9naGRmZmtsZGlzdGFuY2Uxshkhilkdfseyula.jpg
konkurs->competition
...
barbiturát->barbiturate
cache/explanations/cs/c2RmdWlrbG9naGRmZmtsYmFyYml0dXJhdGU1shkhilkdfseyula.txt
cache/images/c2RmdWlrbG9naGRmZmtsYmFyYml0dXJhdGU1shkhilkdfseyula.jpg
```
</details>

   * you can verify by `python caches.py  cs read`
<details>

```
Translation cache content for cs
reding cache/transaltions/cs2en cache
Loaded 32 cache items
32 items
  'neutrál' to en is : neutral
  'čert' to en is : devil
...
  'afganistan' to en is : afghanistan
  'barbiturát' to en is : barbiturate
Explanations cache for cs is cache/explanations/cs
116 items
  'primaballerine3'(537b) saved as: c2RmdWlrbG9naGRmZmtscHJpbWFiYWxsZXJpbmUzshkhilkdfseyula.txt
  'cucumber5'(714b) saved as: c2RmdWlrbG9naGRmZmtsY3VjdW1iZXI1shkhilkdfseyula.txt
  'afghanistan2'(794b) saved as: c2RmdWlrbG9naGRmZmtsYWZnaGFuaXN0YW4yshkhilkdfseyula.txt
  'explanation3'(731b) saved as: c2RmdWlrbG9naGRmZmtsZXhwbGFuYXRpb24zshkhilkdfseyula.txt
..
  'cucumber2'(632b) saved as: c2RmdWlrbG9naGRmZmtsY3VjdW1iZXIyshkhilkdfseyula.txt
  'competition2'(825b) saved as: c2RmdWlrbG9naGRmZmtsY29tcGV0aXRpb24yshkhilkdfseyula.txt
  'translation5'(942b) saved as: c2RmdWlrbG9naGRmZmtsdHJhbnNsYXRpb241shkhilkdfseyula.txt
Image cache (shared for al languages)  is cache/images
116 items
  'neutral1'(27245b) saved as: c2RmdWlrbG9naGRmZmtsbmV1dHJhbDE=shkhilkdfseyula.jpg
  'cucumber2'(52111b) saved as: c2RmdWlrbG9naGRmZmtsY3VjdW1iZXIyshkhilkdfseyula.jpg
  'cottage1'(71941b) saved as: c2RmdWlrbG9naGRmZmtsY290dGFnZTE=shkhilkdfseyula.jpg
  'competition2'(60793b) saved as: c2RmdWlrbG9naGRmZmtsY29tcGV0aXRpb24yshkhilkdfseyula.jpg
 ...
  'prefeeding5'(39411b) saved as: c2RmdWlrbG9naGRmZmtscHJlZmVlZGluZzU=shkhilkdfseyula.jpg
  'conclusion2'(45016b) saved as: c2RmdWlrbG9naGRmZmtsY29uY2x1c2lvbjI=shkhilkdfseyula.jpg
  'afghanistan1'(65626b) saved as: c2RmdWlrbG9naGRmZmtsYWZnaGFuaXN0YW4xshkhilkdfseyula.jpg

```
</details>

   * once you have the content of file cached, yuo can play croswords withiout hours of waiting
   * You can verify content of caches by ` python  caches.py  lang print`. eg ` python  caches.py  cs print` (as all except images are transalted somwhere in process)

## crosswords generation issue:
Soetimes jsut single or two words puzzle is generated. The generation is random, and bad things happen. But there is worse issue:
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
Especially the `word1word2` case with intersection is very confusing, sorry. (as it writes as AAAAABBBBB (where correct is something like AAAAA(AB)BBBB)

# Play
 * `python game.py <file_with_words>`  where file_with_words is  `cs` or some previously cached subset like `python game.py python game.py cs-20-2025-09-05_14\:36\:15`
 * It will generate crosswords puzzle with as much words as you set up  - or default is aprox 5 - to small grid which shoudl fit terminal unless you changed it by  `SIZE` variable
 * you can see that instead of words are theirs IDs. Eg `AAAAA` is first word of length of 5. eg:

<details>

  ```
python game.py  cs-20-2025-09-05_14\:36\:15  3
...

. . . . . . . . C C C C C C C C . . . . . . . .
. . . . . . . . . . . . B . . . . . . . . . . .
. . . . . . . . . . . . B . . . . . D . . . . .
. . . . . . . . . . . . B . . . . . D . . . . .
. . . . . . . . . . . . B . . . . . D . . . . .
. . . . . . . . . . . . B . . . . . D . . . . .
. . . . . . . . . . . . B . . . . . D . . . . .
. . . . . . . . . . . . B . . . . . D . . . . .
. . . . . . . . . . . . B A E A A A D . . . . .
. . . . . . . . . . . . . . E . . . D . . . . .
. . . . . . . . . . . . . . E . . . D . . . . .
. . . . . . . . . . . . . . E . . . D . . . . .
. . . . . . . . . . . . . . E . . . D . . . . .
. . . . . . . . . . . . . . E . . . D . . . . .
. . . . . . . . . . . . . . . . . . D . . . . .
help exit L ? ?n ?? (? ?n ?? I In II T G Tn TT GG newI newT delIn delTn)[a-z] `sub[A-Z] guess`
```
</details>

 * if some of words are missing at least 1 explanation and 1 image, that will be generated.
   *  that is slow. Use `caches.py` to pregenerate hints before playing
 * then you guess words!
   * if you jsut type word, it will apear on place - if correct. eg here `podbíječka` was jsut filled in but `dálkař` was not
  
<details>

  ```
python game.py  cs-20-2025-09-05_14\:36\:15  3
...
podbíječka
help exit L ? ?n ?? (? ?n ?? I In II T G Tn TT GG newI newT delIn delTn)[a-z] `sub[A-Z] guess`
ok!
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . p o d b í j e č k a . . . . . . . .
. . . . . . . . . . . . . . B . . . . . . . . .
. . . . . . . . . . . . . . B . . . C . . . . .
. . . . . . . . . . . . . . B . . . C . . . . .
. . . . . . . . . . . . . . B . . . C . . . . .
. . . . . . . . . . . . A A B A A A C A . . . .
. . . . . . . . . . . . . . D D D D D D . . . .
. . . . . . . . . . . . . . . . . . C . . . . .
. . . . . . . . . . . . . . . . . . C . . . . .
. . . . . . . . . . . . . . . . . . C . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .
dálkař    
help exit L ? ?n ?? (? ?n ?? I In II T G Tn TT GG newI newT delIn delTn)[a-z] `sub[A-Z] guess`
nope:(
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . p o d b í j e č k a . . . . . . . .
. . . . . . . . . . . . . . B . . . . . . . . .
. . . . . . . . . . . . . . B . . . C . . . . .
. . . . . . . . . . . . . . B . . . C . . . . .
. . . . . . . . . . . . . . B . . . C . . . . .
. . . . . . . . . . . . A A B A A A C A . . . .
. . . . . . . . . . . . . . D D D D D D . . . .
. . . . . . . . . . . . . . . . . . C . . . . .
. . . . . . . . . . . . . . . . . . C . . . . .
. . . . . . . . . . . . . . . . . . C . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .

```
</details>

  * you have variety of commands to help you solve the puzzle. From those most mighty is `sub`:

  <details>

  ```
sub dálkař
help exit L ? ?n ?? (? ?n ?? I In II T G Tn TT GG newI newT delIn delTn)[a-z] `sub[A-Z] guess`
injected: 1x
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . p o d b í j e č k a . . . . . . . .
. . . . . . . . . . . . . . B . . . . . . . . .
. . . . . . . . . . . . . . B . . . d . . . . .
. . . . . . . . . . . . . . B . . . á . . . . .
. . . . . . . . . . . . . . B . . . l . . . . .
. . . . . . . . . . . . A A B A A A k A . . . .
. . . . . . . . . . . . . . D D D D a D . . . .
. . . . . . . . . . . . . . . . . . ř . . . . .
. . . . . . . . . . . . . . . . . . C . . . . .
. . . . . . . . . . . . . . . . . . C . . . . .
. . . . . . . . . . . . . . . . . . . . . . . .

```
</details>

  * You can see sub can inject substrings. With AI hints, you are very often sure with some part - like here - but not with whole
  * sub can be directed to exact word. so `subC dálkař` would do. `subA dálkař` would not:
```
? to fill random letter
?number to fill random Nth letter
?[a-z] to fill random letter of selected word
?number[a-z] to fill Nth letter of selected word
?? to random whole word
??[a-z] to fill whole word of given word
L[a-z] length of given word
`sub[A-Z] guess` try to fill matching guess SUBSTRING to selected word
`sub guess` try to fill matching guess SUBSTRING to ALL words (
```
 * eg
   * `?1` will fill fandom first letter
   * `?D` will fill random letter  DDDDDDD
   * `?B1` will fill first letter of word BBBB
   * `??F` will fill give up word FFFF

 
## Getting hints
Each word can be described to you by image or explanmation:
```
I[a-z] to show next image (from all) for given word
T[a-z] to show next hint (from all) for given word
G[a-z] to show next hint (from all) for given word in external window
Inumber[a-z] to show Nth image (from all) for given word
Tnumber[a-z] to show Nth hint (from all) for given word
Gnumber[a-z] to show Nth hint (from all) for given word in external window
II[a-z] to show all images for given word
TT[a-z] to show all texts for given word
GG[a-z] to show all texts for given word in external window
```
 * eg
   * `Ia`  wil show next image for word AAAA
   * `Tb`  wil show next text for word BBBBB
   * `Gb`  wil show next text for word GGGG in standalone window
   * `I3c`  wil show 3rd image for word CCC
   * `T1d`  wil show 1st text for word DDDDDDDD
   * `G2e`  wil show 2nd text for word EEEE in standalone window
   * `IIa`  wil show all images for word AAAA
   * `TTb`  wil show all texts for word BBBBB
   * `GGg`  wil show all texts for word GGGG in standalone window

## Generating hints during runtime
During play, you can run `caches.py` as usually (above same subset file), the freshly cached images/texts will be immediately used
You can generate them also from game itself but it have  issues - frozen gameplay or output to command prompt
```
newsI[a-z] to generate and add new image for given word. Use all instead of a-z to generate all - sync
newsT[a-z] to generate and add new text for given word. Use all instead of a-z to generate all - sync
newI[a-z] to generate and add new image for given word. Use all instead of a-z to generate all - async
newT[a-z] to generate and add new text for given word. Use all instead of a-z to generate all - async
delInumber[a-z] to remove Nth image. Check by In before
delTnumber[a-z] to remove Nth text. Check by Tn before
```
## Playing in headless mode
The game works fine in headlees (no gui, terminal only) mode. Surprisngly better experience is in defaut `ASYNC=True` mode, which consumes more exceptions.
Of course you can not show images, and I'm, not going to reimplemen https://github.com/judovana/ConsoleImageViewer. The images are terrible enough.
Hiowever playing only with text hints, is extreamly difficult, nearly impossible
