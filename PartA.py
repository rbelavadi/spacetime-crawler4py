from pathlib import Path
import sys
alnumset = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', '\'', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

stopwords = set()

def get_stopwords():
    file = open("stopwords.txt", "r")
    word = file.readline()
    while word:
        stopwords.add(word.strip().lower())
        word = file.readline()
# get_stopwords()
    
# O(n) time complexity, O(m) space complexity. n = number of characters, m = number of tokens
def tokenize(text):
    return list(token_gen(text))

# O(n) time complexity, O(k) space complexity. k = largest word
def token_gen(text):
    word_chars = []
    for char in text:
        if char.isalpha():
            c = char.lower()
        else:
            c = char
        if c in alnumset:
            word_chars.append(c)
        else:
            if word_chars:
                yield(''.join(word_chars))
                word_chars = []
    if word_chars:
        yield(''.join(word_chars))
    return []

# O(n) time complexity, O(n) space complexity. n = number of items in tokens.
def computeWordFrequencies(tokens):
    freq_dict = {}
    for token in tokens:
        if len(token) <= 1: # Don't count words less than one
            continue
        if token in stopwords: # Don't count stopwords
            continue
        freq_dict[token] = freq_dict.get(token, 0) + 1
    return freq_dict
    
# O(nlogn) time complexity, O(n) space complexity. n = number of items in dictionary.
def print_f(freqs):
    for token, num in sorted(freqs.items(), key=lambda x: x[1], reverse=True):
        print(token, num)