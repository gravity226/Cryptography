import string
import matplotlib.pyplot as plt
import numpy as np

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


# Main

if __name__ == '__main__':
    text = 'The Vigenere Cipher was developed by mathematician Blaise de Vigenere in the 16th century. The Vigenere Cipher was adapted as a twist on the standard Caesar cipher to reduce the effectiveness of performing frequency analysis on the ciphertext. The cipher accomplishes this using uses a text string (for example, a word) as a key, which is then used for doing a number of alphabet shifts on the plaintext. Similar to the Caesar Cipher, but instead of performing a single alphabet shift across the entire plaintext, the Vigenere cipher uses a key to determine several different shift amounts across the entirety of the message.'
    text = text.replace(' ', '').upper()
    # text = 'THEVIGENERECIPHERWASDEVELOPEDBYMATHEMATICIANBLAISEDEVIGENEREINTHE16THCENTURY.THEVIGENERECIPHERWASADAPTEDASATWISTONTHESTANDARDCAESARCIPHERTOREDUCETHEEFFECTIVENESSOFPERFORMINGFREQUENCYANALYSISONTHECIPHERTEXT.THECIPHERACCOMPLISHESTHISUSINGUSESATEXTSTRING(FOREXAMPLE,AWORD)ASAKEY,WHICHISTHENUSEDFORDOINGANUMBEROFALPHABETSHIFTSONTHEPLAINTEXT.SIMILARTOTHECAESARCIPHER,BUTINSTEADOFPERFORMINGASINGLEALPHABETSHIFTACROSSTHEENTIREPLAINTEXT,THEVIGENERECIPHERUSESAKEYTODETERMINESEVERALDIFFERENTSHIFTAMOUNTSACROSSTHEENTIRETYOFTHEMESSAGE.'

    encrypted_text = encrypt(text=text)

    sup = 'Letter Frequency'
    letter_frequency(sup, text)
















#
