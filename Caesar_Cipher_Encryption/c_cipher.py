import string
import matplotlib.pyplot as plt
import numpy as np

# ------  Encrypt with the Caesar Cipher  ------

# input s is a sentence, one string. ex: s = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
def encrypt(s, key):
    uppers = string.uppercase[:26]
    s1 = ''
    for l in s:
        if l == ' ':
            s1 += ' '
        else:
            new_key = uppers.index(l) + key if uppers.index(l) + key < len(uppers) else uppers.index(l) + key - len(uppers)
            s1 += uppers[new_key]
    return s1


# ------  Frequency  ------

def letter_frequency(sup, s):
    f = np.array( sorted([[s.count(l), l] for l in set(s)], key=lambda z: z[1]) )
    # f = np.array(sorted(f, key=lambda z: z[1]))
    # return f
    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4)
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:])
    plt.suptitle(sup)
    plt.title(s)
    # plt.savefig('encrypted_message.png')
    plt.show()

def word_frequency(sup, s):
    words = s.split()
    f = np.array( sorted([[words.count(w), w] for w in set(words)], key=lambda w: w[1]) )

    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4, color='y')
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:], rotation=45)
    plt.suptitle(sup)
    plt.title(s)
    plt.savefig('wf_encrypted.png')
    plt.show()



if __name__ == '__main__':
    s = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    key = 3
    s1 = encrypt(s, key)

    # sup = 'Original Message <==> Letter Frequency'
    # sup = 'Encrypted Message <==> Key = %i' % key
    # letter_frequency(sup, s1)

    # w_sup = 'Original Message <==> Word Frequency'
    # w_sup = 'Encrypted Message <==> Key = 3'
    # word_frequency(w_sup, s1)












##
