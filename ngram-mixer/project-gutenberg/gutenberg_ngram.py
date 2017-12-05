import sys
import requests
import re
from collections import Counter, OrderedDict
from nltk import ngrams
from itertools import chain  # to flatten list of tuples from zip output
from operator import itemgetter  # fast than lambda for comprehansion
import random

# Find the books ids by looking on Project Gutenberg website in the address bar.
books = {'A Christmas Carol': 46,
         'Pride and Prejudice': 1342,
         'Huckleberry Fin': 76,
         'Sherlock Holmes': 1661,
         'Frankenstein': 84}


def get_ngrams(words, n, use_nltk=True, use_zip=False):
    ''' Use nltk, zip or list comprehension to generate ngrams form list of
    words '''
    if use_nltk:
        n_grams = [' '.join(grams) for grams in ngrams(words, n)]
    elif use_zip:
        n_grams = list(
            chain.from_iterable(zip(*[words[i:] for i in range(n)])))
    else:
        n_grams = [words[i:i + n] for i in range(len(words) - n + 1)]

    # Count the occurence of each ngram in list with dict value
    ngram_counter = Counter(n_grams)

    # Change the key into tuple of words in ngram
    ngram_dict = \
        {tuple(k.split()): ngram_counter[k] for k in ngram_counter}

    # Sort the dict by key value
    ngram_count = OrderedDict(
        sorted(ngram_dict.items(), key=itemgetter(1), reverse=True))

    # print(list(ngram_count.items())[:5])

    return ngram_count


def process_a_book(book_key, ngram_size):
    req = requests.get(
        'https://www.gutenberg.org/files/{0}/{0}.txt'.format(books[book_key]))

    # print(len(req.text), ',', req.text[:50])
    # remove all non letter based tokens
    words = re.split('[^A-z]+', req.text.lower())
    # print(len(words))
    words = list(filter(None, words))  # Remove empty strings

    # Build NGrams count:
    ngrams_counter_sorted = get_ngrams(words, ngram_size)

    return ngrams_counter_sorted


def get_all_books():
    '''Gets all titles from `book` dictionary'''

    # for book in books:
    pass


def get_one_from_many_next_ngrams(ngram_count_dict):
    '''Weighted-probability based on counts '''
    total = sum(count for ngram, count in ngram_count_dict.items())
    r = random.uniform(0, total)
    upto = 0
    for ngram, count in ngram_count_dict.items():
        if upto + count > r:
            return ngram[0]
        upto += count


def generate_ngram_sentence(word, counted_ngrams, sentences_length=10):
    ''' Generates sentences with default size fo 10 starting with given
    `word` '''
    print(list(counted_ngrams.items())[:5])
    sentence = [word]
    next_word = word

    print(sentence)
    for i in range(sentences_length):
        # `()` means generator:
        all_next_words = [rest[-1] for first, *rest in counted_ngrams
                          if first == next_word]
        # print(all_next_words)
        #
        all_next_ngrams = {k: v for k, v in counted_ngrams.items()
                           if k[0] in all_next_words}
        # print('{0}: {1}'.format(len(all_next_ngrams),all_next_ngrams))

        if not all_next_ngrams:
            break
        # Choose a pair with weighted probability from the all_next_ngrams dict
        next_word = get_one_from_many_next_ngrams(all_next_ngrams)

        sentence.append(next_word)

    print(' '.join(sentence))


def generate_sentences(cmd_par):
    arguments_list = cmd_par.split()
    cmd_options = [arg for arg in arguments_list if arg.startswith('-')]
    cmd_params ={'ngram_size': 2, 'sentence_length': 20} # default

    for option in cmd_options:
        if '-ngram-size' in option:
            cmd_params['ngram_size'] = int(option.split('=')[1])
        elif '-sentence-length' in option:
            cmd_params['sentence_length'] = int(option.split('=')[1])
        else:
            print(('Did not recognize the following argument: %s' % option))

    counted_ngrams = process_a_book('Pride and Prejudice',  cmd_params['ngram_size'])
    generate_ngram_sentence('i', counted_ngrams, cmd_params['sentence_length'])


if __name__ == '__main__':
    argumentString = ' '.join(sys.argv[1:])
    try:
        generate_sentences(argumentString)
    except:
        print('ERROR: [Gutenberg_Ngram].')
