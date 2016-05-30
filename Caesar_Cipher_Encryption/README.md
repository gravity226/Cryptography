# Caesar Cipher

### Summary
This is a simple encryption technique where you shift every letter in a document by n spaces.  

### Contents
 - [Encryption](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#encryption)
 - [Letter Frequency](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#letter-frequency)
 - [Word Frequency](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#word-frequency)
 - Decryption

##### Encryption
``` python
import string

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
```

##### Letter Frequency
One technique for decrypting a document is to look at the frequency of the letters used.
```python
import matplotlib.pyplot as plt
import numpy as np

def frequency(s):
    f = np.array( sorted([[s.count(l), l] for l in set(s)], key=lambda z: z[1]) )
    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4)
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:])
    plt.show()
```
<br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/original_message.png" height="400" />
<br />
<br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/encrypted_message.png" height="400" />

##### Word Frequency
What about the word frequency?  Some words are naturally used more than others.
``` python
import matplotlib.pyplot as plt
import numpy as np

def word_frequency(s):
    words = s.split()
    f = np.array( sorted([[words.count(w), w] for w in set(words)], key=lambda w: w[1]) )

    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4, color='y')
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:], rotation=45)
    plt.show()
```
<br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/wf_original.png" height="400" />
<br />
<br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/wf_encrypted.png" height="400" />
