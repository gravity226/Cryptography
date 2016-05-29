import string
import matplotlib.pyplot as plt
import numpy as np

# ------  Encrypt with the Caesar Cipher  ------

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


# ------  Decrypt  ------

def frequency(s):
    f = np.array( [[s.count(l), l] for l in set(s)] )
    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4)
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:])
    plt.show()



if __name__ == '__main__':
    s = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    s1 = encrypt(s, 0)

    frequency(s1)













##
