#About

Some basic idea on how to model a text is with use of n-grams. This code is 
based on resources provided by the 
[Project Gutenberg](https://www.gutenberg.org). The goal of the following 
code is to gather code for custom set of books. Building an n-gram set will 
be useful to build a sentence-like sequences of words basing on the 
constructed n-grams.

### Dependencies

* Python 3
* requests
* nltk
* itertools
* operator
* random

# Running
```
$ python3 gutenberg_ngram.py -sentence-length=30 -ngram-size=3
```

If run without parameters the default generated sentence length is 20 and size
 of n-gram is 2.

