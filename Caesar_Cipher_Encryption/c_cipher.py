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

def letter_frequency(sup, s):
    f = np.array( [[s.count(l), l] for l in set(s)] )
    f = np.array(sorted(f, key=lambda z: z[1]))
    # return f
    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4)
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:])
    plt.suptitle(sup)
    plt.title(s)
    plt.savefig('encrypted_message.png')
    plt.show()



if __name__ == '__main__':
    s = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    key = 3
    s1 = encrypt(s, key)

    # sup = 'Original Message <==> Letter Frequency'
    # sup = 'Encrypted Message <==> Key = %i' % key
    # letter_frequency(sup, s1)













##
