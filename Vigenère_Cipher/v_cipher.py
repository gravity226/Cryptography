from __future__ import division

import string
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Globals

letters = string.uppercase[:26] + "!@#$%^&*()_+-=,./<>?'1234567890"
# letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=,./<>?'1234567890"


# Methods

def encrypt(text, key='TOMMY'):
    encrypted_text = ''
    for n in xrange(len(text)):
        en = letters.index(text[n])
        adding = n % len(key)

        new_letter = en + adding

        if new_letter > len(letters):
            encrypted_text += letters[new_letter - len(letters)]
        else:
            encrypted_text += letters[new_letter]

    return encrypted_text

def letter_frequency(sup, s):
    f = np.array( sorted([[s.count(l), l] for l in set(s)], key=lambda z: z[1]) )
    # f = np.array(sorted(f, key=lambda z: z[1]))
    # return f
    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4)
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:])
    plt.suptitle(sup)
    # plt.title(s)
    plt.savefig('original_message.png')
    plt.show()

def coincidences(encrypted_text):
    pattern = []
    for a in xrange(1, len(encrypted_text)):
        count = 0
        for b, c in zip(encrypted_text[a:], encrypted_text[:-a]):
            if b == c:
                count += 1
        pattern.append(count)

    # plt.plot(pattern[:40])
    # plt.savefig('key_length_pattern.png')
    # plt.show()

    return pattern

def find_key_length(encrypted_text):
    pattern = coincidences(encrypted_text)

    distances = []
    last = 0
    for x in xrange(1, len(pattern)-1):
        if pattern[x] > pattern[x-1] and pattern[x] > pattern[x+1]:
            distances.append(x - last)
            last = x

    plt.plot(distances)
    # plt.savefig('key_length.png')
    plt.show()

    print Counter(distances).most_common(5)

def get_char_freq():
    with open("characters.txt") as f:
        data = {}
        for line in f:
            x = line.split()
            print line
            data[x[1]] = float(x[-1].replace('%)', '').replace('\n', '').replace('(', '')) * .01

    freqs = {}
    for a, b in zip(string.uppercase[:26], string.lowercase[:26]):
        freqs[a] = data[a] + data[b]

    for c in "!@#$%^&*()_+-=,./<>?'1234567890":
        freqs[c] = data[c]

    return freqs

def get_encrypted_freq(encrypted_text):
    uniques = {}
    for a in set(encrypted_text):
        uniques[a] = encrypted_text.count(a) / len(encrypted_text)

    return uniques


# Main

if __name__ == '__main__':
    text = 'The Vigenere Cipher was developed by mathematician Blaise de Vigenere in the 16th century. The Vigenere Cipher was adapted as a twist on the standard Caesar cipher to reduce the effectiveness of performing frequency analysis on the ciphertext. The cipher accomplishes this using uses a text string (for example, a word) as a key, which is then used for doing a number of alphabet shifts on the plaintext. Similar to the Caesar Cipher, but instead of performing a single alphabet shift across the entire plaintext, the Vigenere cipher uses a key to determine several different shift amounts across the entirety of the message.'
    text = text.replace(' ', '').upper()
    # text = 'THEVIGENERECIPHERWASDEVELOPEDBYMATHEMATICIANBLAISEDEVIGENEREINTHE16THCENTURY.THEVIGENERECIPHERWASADAPTEDASATWISTONTHESTANDARDCAESARCIPHERTOREDUCETHEEFFECTIVENESSOFPERFORMINGFREQUENCYANALYSISONTHECIPHERTEXT.THECIPHERACCOMPLISHESTHISUSINGUSESATEXTSTRING(FOREXAMPLE,AWORD)ASAKEY,WHICHISTHENUSEDFORDOINGANUMBEROFALPHABETSHIFTSONTHEPLAINTEXT.SIMILARTOTHECAESARCIPHER,BUTINSTEADOFPERFORMINGASINGLEALPHABETSHIFTACROSSTHEENTIREPLAINTEXT,THEVIGENERECIPHERUSESAKEYTODETERMINESEVERALDIFFERENTSHIFTAMOUNTSACROSSTHEENTIRETYOFTHEMESSAGE.'

    encrypted_text = encrypt(text=text)

    sup = 'Letter Frequency'
    # letter_frequency(sup, text)
    # coincidences(encrypted_text)
    find_key_length(encrypted_text)
    uniques = get_encrypted_freq(encrypted_text)
















#
